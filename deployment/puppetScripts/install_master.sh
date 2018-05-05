#!/bin/bash

source puppet.config
source util.sh

auto-retry ssh -i $pem_file ec2-user@$master_dns /bin/bash << 'ENDHERE' 
    sudo su
    hostname master.devops.org
    yum -y install https://yum.puppetlabs.com/puppetlabs-release-pc1-el-7.noarch.rpm
    yum -y install puppetserver
    /opt/puppetlabs/bin/puppet module install puppetlabs-vcsrepo --version 2.3.0
    iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
    iptables -A INPUT -m state --state NEW -p tcp --dport 8140 -j ACCEPT
    iptables-save
    iptables -L -v
    sudo sed -i "s/Xmx2g/Xmx900m/" /etc/sysconfig/puppetserver
    sudo sed -i "s/Xms2g/Xms900m/" /etc/sysconfig/puppetserver
    echo "Starting puppet server"
    systemctl enable puppetserver
    systemctl start puppetserver
    exit
ENDHERE
