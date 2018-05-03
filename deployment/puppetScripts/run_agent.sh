#!/bin/bash

source puppet.config
source util.sh

auto-retry ssh -i $pem_file ec2-user@$agent_dns /bin/bash << 'ENDHERE'
    sudo su
    /opt/puppetlabs/bin/puppet agent --test --ca_server=master.devops.org
    exit
ENDHERE


