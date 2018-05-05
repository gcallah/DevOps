#!/bin/bash

source puppet.config
source util.sh

auto-retry ssh -i $pem_file ec2-user@$master_dns /bin/bash <<- 'ENDHERE' 
    sudo su
    echo "Listing certificates"
    certlist=""
    while [ -z "$certlist" ]; do
        certlist=$(/opt/puppetlabs/bin/puppet cert list) 
    done
    echo "Signing certificates"
    /opt/puppetlabs/bin/puppet cert sign agent.devops.org
    echo "Writing to apache.pp"

    TEXT="
    package { 'httpd':
        ensure => installed,
    }
    service { 'httpd':
        ensure => running
    }"

    echo "$TEXT" > /etc/puppetlabs/code/environments/production/manifests/apache.pp

    echo "Writing to site.pp"
    TEXT="
    package { 'git' :
        ensure => present,
    }
    vcsrepo { '/var/www/html':
        ensure   => latest,
        provider => git,
        source   => 'http://github.com/gcallah/DevOps.git',
        revision => 'master',
    }"
    echo "$TEXT" > /etc/puppetlabs/code/environments/production/manifests/site.pp  
    
    exit
ENDHERE

