import sys
import os
import boto3
from botocore.exceptions import ClientError
import constants

def enter_host(dns, ip, hostnames, file):
    command = (
'ssh -i %s ec2-user@%s -oStrictHostKeyChecking=no /bin/bash << \'ENDHERE\'\n'
'    sudo su\n'
'    found=$(grep %s /etc/hosts)\n'
'    if [ -z "$found" ]; then\n'
'        echo \"%s %s\" >> /etc/hosts\n'
'    fi\n'
'    exit\n'
'ENDHERE' % (file, dns, ip, ip, hostnames))
    os.system(command)

def main(create_instance):
    #Creating Key Pairs
    ec2_client = boto3.client('ec2',
        region_name=constants.REGION)
    try:
        key_pair = ec2_client.describe_key_pairs(
            KeyNames=[constants.KEY_PAIR])
        print("EXISTING KEY PAIR")
    except ClientError as e:
        os.system("echo 'yes' | rm '%s.pem' &> /dev/null"
                  % constants.KEY_PAIR)
        out_file = open(constants.KEY_PAIR+'.pem','w')
        key_pair = ec2_client.create_key_pair(
            KeyName=constants.KEY_PAIR)
        out_content = str(key_pair['KeyMaterial'])
        print("Key PAIR CREATED")
        out_file.write(out_content)
        out_file.close()
        os.system('chmod 0400 %s.pem' % constants.KEY_PAIR)
    
    #Creating Security Groups
    try:
        response = ec2_client.describe_security_groups(
            GroupNames=[constants.SECURITY_GROUP])
    except ClientError as e:
        vpc_id = ec2_client.describe_vpcs().get('Vpcs', [{}])[0].get('VpcId', '')
        security_group = ec2_client.create_security_group(
            GroupName=constants.SECURITY_GROUP,
            Description='Security group for puppet deployment instances',
            VpcId=vpc_id)
        security_group_id = security_group['GroupId']
        data = ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 80,
                 'ToPort': 80,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 22,
                 'ToPort': 22,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 8140,
                 'ToPort': 8140,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
    
    s_grp_id = ec2_client.describe_security_groups(
         GroupNames=[constants.SECURITY_GROUP]).get(
         'SecurityGroups', [{}])[0].get('GroupId', '')
    vpc_id = ec2_client.describe_vpcs().get('Vpcs', [{}])[0].get('VpcId', '')
    ec2 = boto3.resource('ec2')
    if create_instance:
        instances = ec2.create_instances(ImageId=constants.IMAGE_ID,
                            MinCount=constants.MIN_COUNT,
                            MaxCount=constants.MAX_COUNT,
                            KeyName=constants.KEY_PAIR,
                            SecurityGroupIds=[s_grp_id],
                            InstanceType=constants.INSTANCE_TYPE)
        #Connecting to instances
        print("Waiting for instances to initialize")
        waiter = ec2_client.get_waiter('instance_status_ok')
        waiter.wait(Filters=[
                    {
                        'Name': 'instance-state-name',
                        'Values': [
                            'running'
                        ]
                    },
                ],
                WaiterConfig={
                'Delay': 30,
                'MaxAttempts': 50
                })
        print("All instances have been initialized")
    response = ec2_client.describe_instances(Filters=[
            {
                'Name': 'image-id',
                'Values': [
                    constants.IMAGE_ID,
                ]
            },
            {
                'Name': 'instance-state-name',
                'Values': [
                    'running'
                ]
            },
        ])
    reservations = response.get('Reservations')
    
    instance_count = 0
    master_ip = None
    agent_ip = None
    master_dns = None
    agent_dns = None
    for reservation in reservations:
        instances = reservation.get('Instances')   
        for instance in instances:
            instance_id = instance.get('InstanceId')
            dns = instance.get('PublicDnsName')
            private_ip = instance.get('PrivateIpAddress')
            instance_count += 1
            if instance_count == 1:
                master_dns = dns
                master_ip = private_ip
            else:
                agent_dns = dns
                agent_ip = private_ip
    
    os.system('rm puppet.config')
    os.system('echo "master_ip=%s" >> puppet.config' % master_ip)
    os.system('echo "master_dns=%s" >> puppet.config' % master_dns)
    os.system('echo "agent_ip=%s" >> puppet.config' % agent_ip)
    os.system('echo "agent_dns=%s" >> puppet.config' % agent_dns)
    os.system('echo "pem_file=%s" >> puppet.config' %
        (constants.KEY_PAIR + '.pem'))
    
    print("Editing /etc/hosts in master")
    enter_host(master_dns, agent_ip, "agent.devops.org agent",
        constants.KEY_PAIR + '.pem')
    
    print("Editing /etc/hosts in agent")
    enter_host(agent_dns, master_ip, "master.devops.org master",
        constants.KEY_PAIR + '.pem')
    
    if create_instance:
        print("Installing master")
        os.system('./install_master.sh')
        print("Installing agent")
        os.system('./install_agent.sh')
        print("Running master")
        os.system('./run_master.sh')
    print("Running agent")
    os.system('./run_agent.sh')
    
    print("Website Link: http://%s" % agent_dns)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "nocreate":
        create_instance = False
    else:
        create_instance = True

    main(create_instance)
