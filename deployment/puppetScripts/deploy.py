import sys
import os
import subprocess
import boto3
from botocore.exceptions import ClientError
import time

REGION = 'us-east-1'
KEY_PAIR = 'puppetkey'
SECURITY_GROUP = 'puppetsg'
INSTANCE_DETAILS = {
"imageID": "ami-6871a115",
"minCount": 1,
"maxCount": 2,
"keyName": KEY_PAIR,
"securityGroups": SECURITY_GROUP,
"instanceType": "t2.micro"
}
CREATE=False

def enter_host(dns, ip, hostnames, file):
    command = (
'ssh -i %s ec2-user@%s /bin/bash << \'ENDHERE\'\n'
'    sudo su\n'
'    found=$(grep %s /etc/hosts)\n'
'    if [ -z "$found" ]; then\n'
'        echo \"%s %s\" >> /etc/hosts\n'
'    fi\n'
'    exit\n'
'ENDHERE' % (file, dns, ip, ip, hostnames))
    print(command)
    os.system(command)

#Creating Key Pairs
ec2_client = boto3.client('ec2', region_name=REGION)
try:
    existing_pair = ec2_client.describe_key_pairs(KeyNames=[KEY_PAIR])
    print(existing_pair)
except ClientError as e:
    #print(e)
    print("Key pair not found")
    out_file = open(KEY_PAIR+'.pem','w')
    key_pair = ec2_client.create_key_pair(KeyName=KEY_PAIR)
    out_content = str(key_pair['KeyMaterial'])
    out_file.write(out_content)
    print("Created key pair")
subprocess.call(['chmod', '0400', KEY_PAIR+'.pem'])

#Creating Security Groups
try:
    response = ec2_client.describe_security_groups(GroupNames=[SECURITY_GROUP])
    #print(response)
except ClientError as e:
    #print(e)
    vpc_id = ec2_client.describe_vpcs().get('Vpcs', [{}])[0].get('VpcId', '')
    security_group = ec2_client.create_security_group(GroupName=SECURITY_GROUP,
                                         Description='Security group for puppet deployment instances',
                                         VpcId=vpc_id)
    security_group_id = security_group['GroupId']
    print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))
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
    print('Ingress Successfully Set %s' % data)

s_grp_id = ec2_client.describe_security_groups(GroupNames=[INSTANCE_DETAILS['securityGroups']]).get('SecurityGroups', [{}])[0].get('GroupId', '')
print(s_grp_id)
print(INSTANCE_DETAILS['imageID'])
vpc_id = ec2_client.describe_vpcs().get('Vpcs', [{}])[0].get('VpcId', '')
ec2 = boto3.resource('ec2')
if CREATE:
    instances = ec2.create_instances(ImageId=INSTANCE_DETAILS['imageID'],
                        MinCount=INSTANCE_DETAILS['minCount'],
                        MaxCount=INSTANCE_DETAILS['maxCount'],
                        KeyName=INSTANCE_DETAILS['keyName'],
                        SecurityGroupIds=[s_grp_id],
                        InstanceType=INSTANCE_DETAILS['instanceType'])
    #Connecting to instances
    print("WAITING FOR INSTANCES TO INITIALIZE")
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
    print("ALL INSTANCES INITIALIZED")
response = ec2_client.describe_instances(Filters=[
        {
            'Name': 'image-id',
            'Values': [
                INSTANCE_DETAILS['imageID'],
            ]
        },
        {
            'Name': 'instance-state-name',
            'Values': [
                'running'
            ]
        },
    ])
#print(response)
reservations = response.get('Reservations')
print("RESERVATIONS in response")
print(reservations)

instance_count = 0
#print(instances)
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
        print(private_ip)
        print(instance)
        print(dns)

os.system('rm puppet.config')
os.system('echo "master_ip=%s" >> puppet.config' % master_ip)
os.system('echo "master_dns=%s" >> puppet.config' % master_dns)
os.system('echo "agent_ip=%s" >> puppet.config' % agent_ip)
os.system('echo "agent_dns=%s" >> puppet.config' % agent_dns)
os.system('echo "pem_file=%s" >> puppet.config' % (KEY_PAIR + '.pem'))

print("EDITING HOST OF MASTER")
enter_host(master_dns, agent_ip, "agent.devops.org agent", KEY_PAIR + '.pem')

print("EDITING HOST OF AGENT")
enter_host(agent_dns, master_ip, "master.devops.org master", KEY_PAIR + '.pem')

print("INSTALL MASTER")
os.system('./install_master.sh')
print("INSTALL AGENT")
os.system('./install_agent.sh')
print("RUN MASTER")
os.system('./run_master.sh')
print("RUN AGENT")
os.system('./run_agent.sh')
