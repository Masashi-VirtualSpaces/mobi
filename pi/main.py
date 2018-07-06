import s3_worker
import dynamo_worker
import subprocess
import time

#Code for S3
mys3_worker = s3_worker.s3_worker("../credentials.json")
#mys3_worker.create_bucket()
#key = mys3_worker.add_to_bucket('test_images/love_ctk.jpg')
#print("MY KEY: ",key)




command = "fswebcam -r 1280x1024 --no-banner ./images/"
#test"
#jpg"
start = 0
#mys3_worker = s3_worker.s3_worker("../credentials.json")
#mys3_worker.create_bucket()
while(1):
    now = time.time()
    filename = "test"+str(now)+".jpg"
    newimage = command+filename
    test = subprocess.getoutput(newimage)
    print(test)
    key = mys3_worker.add_to_bucket('./images/'+filename)
    print("MY KEY: ",key)
    start += 1
    
    time.sleep(10)


#Code for DynamoDb BELOW

#mydynamo_worker = dynamo_worker.dynamo_worker("../credentials.json")
#mydynamo_worker.addItem()
#mydynamo_worker.getItem()
#mydynamo_worker.updateItem()
#mydynamo_worker.getItem()