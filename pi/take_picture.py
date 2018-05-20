''' This program takes a picture using the Raspberry Pi Camera module'''

from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.start_preview()
sleep(5)
camera.capture('/tmp/picture.jpg')
camera.stop_preview()
#hello 
