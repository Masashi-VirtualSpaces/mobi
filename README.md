# mobi
Repo for IoT 2018 class parking project.
In order to connect to your s3 bucket you need to first run the files in this order...

pi_setup.py
main.py

in order to connect to s3 you must also add your AWS credentials to a file called credentials.json in the root directory in the fields:
```json

{
    "ACCESS_KEY_ID" : "<YOUR AWS ACCESS KEY>",
    "AWS_SECRET_KEY" :"<YOUR AWS SECRET KEY>"
}

```
the file must be named and formatted correctly for the .gitignore and other functions to recognize it.