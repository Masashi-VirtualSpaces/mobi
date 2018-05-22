import boto3
import json
import time

#read json credential files


DEVICE_INFO = None
ACCESS_KEY_ID = None
AWS_SECRET_KEY = None

with open('../credentials.json') as credentials:
    info = json.load(credentials)
    ACCESS_KEY_ID = info['ACCESS_KEY_ID']
    AWS_SECRET_KEY = info['AWS_SECRET_KEY']

with open('device_info.json') as json_file:
    DEVICE_INFO = json.load(json_file)

print(DEVICE_INFO)
print(ACCESS_KEY_ID)
print(AWS_SECRET_KEY)

s3 = boto3.client(
    's3',
    # Hard coded strings as credentials, not recommended.
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_KEY
)

with open('test_images/love_ctk.jpg', 'rb') as data:
    now = time.time()
    key = DEVICE_INFO['name']+':'+str(now)+'.png'
    s3.upload_fileobj(data, DEVICE_INFO['s3_name'], key)