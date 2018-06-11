import boto3
import json
import time
import os

class s3_worker:
    '''
    ABOUT: Worker used to interface with the bucket associated to the device.
    '''
    def __init__(self, credential_file):
        
        with open('../credentials.json') as credentials:
            info = json.load(credentials)
            
            self.DEVICE_ID = info['id']
            self.DEVICE_BUCKET = info['bucketname']

            print(self.DEVICE_BUCKET)
            print(self.DEVICE_ID)
            self.s3 = boto3.client(
                's3',
                aws_access_key_id=info['ACCESS_KEY_ID'],
                aws_secret_access_key=info['AWS_SECRET_KEY']
            )
        #add dynamoDB worker

    def create_bucket(self):
        response = self.s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        print("About to create bucket...")
        if self.DEVICE_BUCKET not in buckets:
            self.s3.create_bucket(Bucket=self.DEVICE_BUCKET,CreateBucketConfiguration={
                'LocationConstraint': 'us-west-2'})
            print("Bucket creation Successful")
        else:
            print("Bucket already exists")

        response = self.s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        print("Bucket List: %s" % buckets)
                
    def add_to_bucket(self,file_path):
        with open(file_path, 'rb') as data:
            #grab file at end of path
            file_name = os.path.basename(file_path)
            now = time.time()
            key = file_name+':'+str(now)+'.png'
            print("Adding file: ",key)
            self.s3.upload_fileobj(data, self.DEVICE_BUCKET, key)
            print("file added")
            return key

