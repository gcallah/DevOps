#!/bin/bash

source puppet.config
source util.sh

auto-retry ssh -i $pem_file ec2-user@$agent_dns /bin/bash << 'ENDHERE'
    sudo su
    hostname agent.devops.org
    echo "Installing packages"
    yum -y install https://yum.puppetlabs.com/puppetlabs-release-pc1-el-7.noarch.rpm
    yum -y install puppet-agent
    exists=$(grep "server = master.devops.org" /etc/puppetlabs/puppet/puppet.conf)
    cp /etc/puppetlabs/puppet/puppet.conf /etc/puppetlabs/puppet/puppet.conf.bak
    if [ -z "$exists" ]; then
      echo "Writing to puppet.conf"
      TEXT="
      server = master.devops.org
      runinterval = 30
      certname = agent.devops.org"
      echo "$TEXT" > /etc/puppetlabs/puppet/puppet.conf
    else
      echo "puppet.conf already configured."
    fi
    systemctl start puppet.service
    systemctl enable puppet.service
    exit
ENDHERE


