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


#connect to s3 database
s3 = boto3.client(
    's3',
    # Hard coded strings as credentials, not recommended.
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Call S3 to list current buckets
response = s3.list_buckets()

# Get a list of all bucket names from the response
buckets = [bucket['Name'] for bucket in response['Buckets']]

# Print out the bucket list
print("Bucket List: %s" % buckets)

#create bucket
if DEVICE_INFO['bucket_name'] not in buckets:
    now = time.time()
    new_bucket = DEVICE_INFO['bucket_name']+str(now)
    s3.create_bucket(Bucket=new_bucket,CreateBucketConfiguration={
        'LocationConstraint': 'us-west-2'})
    
    DEVICE_INFO['s3_name']=new_bucket
    out_file = open("device_info.json","w")
    json.dump(DEVICE_INFO,out_file, indent=4)                                  
    out_file.close()


response = s3.list_buckets()
buckets = [bucket['Name'] for bucket in response['Buckets']]
print("Bucket List: %s" % buckets)
