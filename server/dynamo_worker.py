import boto3
import json
import time
import os

class dynamo_worker:
    '''
    ABOUT: Worker used to interface with the bucket associated to the device.
    '''
    def __init__(self):
        '''
        with open('../credentials.json') as credentials:
            info = json.load(credentials)
            self.DEVICE_ID = info['id']
            self.DEVICE_BUCKET = info['bucketname']

        print(self.DEVICE_BUCKET)
        print(self.DEVICE_ID)
        '''
        self.session = boto3.Session(
            aws_access_key_id='AKIAI63GJPCAORU6HSXA',
            aws_secret_access_key='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'
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
                'taken':0,
                'size':14,
                'available':14
            }
        )

    def getItem(self):
        now = time.time()
        #key = file_name+':'+str(now)+'.png'
        item_name = "masashi"+str(now)
        response = self.dynamoTable.get_item(Key={
            'parking_id':"test11528685120.391113"
            })
        tableInfo = response["Item"]
        print(tableInfo)

    def updateItem(self, taken, available):
        response = self.dynamoTable.update_item(
            Key={
                'parking_id': "test11528685120.391113",
            },
            UpdateExpression="set available= :r, taken= :p",
            ExpressionAttributeValues={
                ':r': taken,
                ':p': available
            },
            ReturnValues="UPDATED_NEW"
        )
