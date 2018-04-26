import sys
import subprocess
import boto3
from botocore.exceptions import ClientError

#Creating Key Pairs
ec2_client = boto3.client('ec2', region_name="us-east-1")
try:
    existing_pair = ec2_client.describe_key_pairs(KeyNames=['puppetwebapp'])
    print(existing_pair)
except ClientError as e:
    print(e)
    print("Key pair not found")
    out_file = open('puppet.pem','w')
    key_pair = ec2_client.create_key_pair(KeyName='puppetwebapp')
    out_content = str(key_pair['KeyMaterial'])
    out_file.write(out_content)
    print("Created key pair")
subprocess.call(['chmod', '0400', 'puppet.pem'])

#Creating Security Groups
try:
    response = ec2_client.describe_security_groups(GroupNames=['puppetdeploy'])
    print(response)
except ClientError as e:
    print(e)
    vpc_id = ec2_client.describe_vpcs().get('Vpcs', [{}])[0].get('VpcId', '')
    security_group = ec2_client.create_security_group(GroupName='puppetdeploy',
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
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])
    print('Ingress Successfully Set %s' % data)

if len(sys.argv) < 1:
    print('Please input the config file')
    sys.exit(1)
else:
    instance_param = {
      "imageID": "ami-6871a115",
      "minCount": 1,
      "maxCount": 2,
      "placement": { "AvailabilityZone": "us-east-1a" },
      "keyName": "puppetwebapp",
      "securityGroups": "puppetdeploy",
      "instanceType": "t2.micro"
    }
    s_grp_id = ec2_client.describe_security_groups(GroupNames=[instance_param['securityGroups']]).get('SecurityGroups', [{}])[0].get('GroupId', '')
    print(s_grp_id)
    print(instance_param['imageID'])
    vpc_id = ec2_client.describe_vpcs().get('Vpcs', [{}])[0].get('VpcId', '')
    ec2 = boto3.resource('ec2')
    instances = ec2.create_instances(ImageId=instance_param['imageID'],
                        MinCount=instance_param['minCount'],
                        MaxCount=instance_param['maxCount'],
                        KeyName=instance_param['keyName'],
                        SecurityGroupIds=[s_grp_id],
                        InstanceType=instance_param['instanceType'])
