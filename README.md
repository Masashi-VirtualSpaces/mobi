# mobi
Repo for IoT 2018 class parking project.


In order to connect to your s3 bucket you need to first run the files in this order...

pi_setup.py
create_bucket.py
add_to_bucket.py

in order to connect to s3 you must also create a file called credentials.json in the root directory with the content structure:
'''

{
    "ACCESS_KEY_ID" : "\<YOUR AWS ACCESS KEY\>",
    "AWS_SECRET_KEY" :"\<YOUR AWS SECRET KEY\>"
}

'''
the file must be named and formatted correctly for the .gitignoreand functions to recognize it.