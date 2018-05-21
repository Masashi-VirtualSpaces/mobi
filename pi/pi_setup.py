'''
Masashi 5/20/18
Use this file to create a script that initializes AWS credentials and sets up a connection to 
the AWS IoT Dashboard.


'''
import json

DEVICE_INFO={}

name = input("What is the device name?\n")
DEVICE_INFO['name']=name

bucket_name = input("What is the bucketname?\n")
DEVICE_INFO['bucket_name'] = bucket_name


out_file = open("device_info.json","w")
json.dump(DEVICE_INFO,out_file, indent=4)                                  
out_file.close()
