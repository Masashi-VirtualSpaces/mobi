import boto3
import json
import time
import os

class dynamo_worker:
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
        self.session = boto3.Session(
            aws_access_key_id=info['ACCESS_KEY_ID'],
            aws_secret_access_key=info['AWS_SECRET_KEY']
        )
        self.dynamo = self.session.resource("dynamodb")
        self.dynamoTable = self.dynamo.Table("parking_lot")

        #add dynamoDB worker

    def addItem(self):
        now = time.time()
        #key = file_name+':'+str(now)+'.png'
        item_name = "masashi"+str(now)
        self.dynamoTable.put_item(
            Item = 
            {
                'parking_id':item_name,
                'key2': "This is a test",
                'size':10,
                'taken':0
            }
        )

    def getItem(self):
        now = time.time()
        #key = file_name+':'+str(now)+'.png'
        item_name = "masashi"+str(now)
        response = self.dynamoTable.get_item(Key={
            'parking_id':"masashi1528664839.2524118"
            })
        tableInfo = response["Item"]
        print(tableInfo)

    def updateItem(self):
        response = self.dynamoTable.update_item(
            Key={
                'parking_id': "masashi1528664839.2524118",
            },
            UpdateExpression="set  taken= :r",
            ExpressionAttributeValues={
                ':r': 3,
            },
            ReturnValues="UPDATED_NEW"
        )