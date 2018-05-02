#!/bin/bash

source puppet.config

ssh -i $pem_file ec2-user@$agent_dns /bin/bash << 'ENDHERE'
    sudo su
    #systemctl start puppet.service
    #systemctl enable puppet.service
    #/opt/puppetlabs/bin/puppet agent --test --ca_server=master.devops.org
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


