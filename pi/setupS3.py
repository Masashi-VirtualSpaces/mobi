import s3_worker
import dynamo_worker
import subprocess
import time

mys3_worker = s3_worker.s3_worker("../credentials.json")
mys3_worker.create_bucket()