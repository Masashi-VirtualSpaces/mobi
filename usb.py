import subprocess
import os
import time 
command = "fswebcam --no-banner ./images/test"
#jpg"
start = 0
while(start!=6):
    now = time.time()
    newimage = command+str(now)+".jpg"
    test = subprocess.getoutput(newimage)
    print(test)
    start += 1
    time.sleep(10)
