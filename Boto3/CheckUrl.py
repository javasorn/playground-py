#python 3
import boto3
import time
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from botocore.exceptions import ClientError

someurl = 'http://www.XXXXX.XX.XXX/'
ec2 = boto3.client('ec2')

# Global Class Pattern
class Mem:
    # Declare globals here...
    instance_id = "i-XXXXXXXXXXXXX"

# Stop the instance
def stop_ec2():
    # This code is from Amazon's EC2 example
    # Do a dryrun first to verify permissions
    try:
        ec2.stop_instances(InstanceIds=[Mem.instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, call stop_instances witout dryrun
    try:
        response = ec2.stop_instances(InstanceIds=[Mem.instance_id], DryRun=False)
        print(response)
    except ClientError as e:
        print(e)

# Start the instance
def start_ec2():
    # This code is from Amazon's EC2 example
    # Do a dryrun first to verify permissions
    try:
        ec2.start_instances(InstanceIds=[Mem.instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, run start_instances without dryrun
    try:
        response = ec2.start_instances(InstanceIds=[Mem.instance_id], DryRun=False)
        print(response)
    except ClientError as e:
        print(e)

def stop_while_stopped_then_start_ec2():
    stop_ec2()
    stoping_ec2 = boto3.resource('ec2')
    while stoping_ec2.Instance(Mem.instance_id).state['Name'] != "stopped":
        print('Instance is still being Stopped')
        time.sleep(5)
    else:
        print('Now instance is Stopped!!!')
        start_ec2()

req = Request(someurl)

try:
    response = urlopen(req)
except HTTPError as e:
    print('The server couldn\'t fulfill the request.')
    print('Error code: ', e.code)
    stop_while_stopped_then_start_ec2()
except URLError as e:
    print('We failed to reach a server.')
    print('Reason: ', e.reason)
    stop_while_stopped_then_start_ec2()
else:
    print('ok')