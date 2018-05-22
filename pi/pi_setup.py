'''
Masashi 5/20/18
Use this file to create a script that initializes AWS credentials and sets up a connection to 
the AWS IoT Dashboard.
'''
import json
import time

DEVICE_INFO={}

#configure name
name = input("What is the device id?\n")
DEVICE_INFO['id']=name

#configure bucket name
bucket_name = name+str(time.time())
DEVICE_INFO['bucketname'] = bucket_name

#Add blank spot for AWS Credentials
DEVICE_INFO['ACCESS_KEY_ID']=""
DEVICE_INFO['AWS_SECRET_KEY']=""

out_file = open("../credentials.json","w")
json.dump(DEVICE_INFO,out_file, indent=4)                                  
out_file.close()