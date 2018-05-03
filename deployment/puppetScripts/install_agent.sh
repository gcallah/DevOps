#!/bin/bash

source puppet.config


ssh -i $pem_file ec2-user@$agent_dns /bin/bash << 'ENDHERE'
    sudo su
    hostname agent.devops.org
    echo "Installing packages"
    yum -y install https://yum.puppetlabs.com/puppetlabs-release-pc1-el-7.noarch.rpm
    yum -y install puppet-agent
    exists=$(grep "server = master.devops.org" /etc/puppetlabs/puppet/puppet.conf)
    cp /etc/puppetlabs/puppet/puppet.conf /etc/puppetlabs/puppet/puppet.conf.bak
    if [ -z "$exists" ]; then
      echo "Writing to puppet.conf"
      echo "server = master.devops.org" >> /etc/puppetlabs/puppet/puppet.conf
      echo "runinterval = 30" >> /etc/puppetlabs/puppet/puppet.conf
    else
      echo "puppet.conf already configured."
    fi
    systemctl start puppet.service
    systemctl enable puppet.service
    echo "Removing entry"
    find /etc/puppetlabs/puppet/ssl -name agent.devops.org.pem -delete
    failure="failed"
    while [ $failure == "failed" ]; do
      echo "Running puppet agent"
      output=$(/opt/puppetlabs/bin/puppet agent --test --ca_server=master.devops.org 2>&1)
      output_list=(${output})
      failure=${output_list[12]} 
      echo $output
      sleep 1
    done
    exit
ENDHERE


