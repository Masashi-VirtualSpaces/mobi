import boto3


def lambda_handler(event, context):
    # TODO implement
    s3 = boto3.client('s3')
    
    
    if event:
        print('Event :', event)
        file_obj = event["Records"][0]
        filename = str(file_obj ['s3']['object']['key'])
        print("Filename : ",filename)
        #What does the key represent??? and how could it be used?
        
        file_obj = s3.get_object(Bucket = "exampleross", Key = filename)
        print("File Obj : ", file_obj)
        file_content = file_obj["Body"].read().decode("utf-8")
        print(file_content)
    
    
    
    print('I am being triggered')
    return 'Hello from Lambda'
