# -*- coding: utf-8 -*-

# This is proof-of-concept code for the Mobi Parking Project
# adapted from GitHub User andrewssobral's haarcascades vehicle detection program
# Last Edit: 6/3/12518 by Ross Hartley

import cv2
import csv
print(cv2.__version__)

def getData():
    with open('data.csv', 'r') as myfile:
        reader = csv.reader(myfile)
        rows = [r for r in reader]
        width = int(rows[0][1])
        height = int(rows[1][1])
        spaces = []
        iter = 0
        for i  in range(2, len(rows)):
            spaces.append({'origin_x': int(rows[i][0]), 'origin_y': int(rows[i][1]), 'id': iter})
            iter += 1
            spaces.append({'origin_x': int(rows[i][0]), 'origin_y': int(rows[i][1])-height, 'id': iter})
            iter += 1
    return width, height, spaces

SPOT_W, SPOT_H, spaces = getData()
cars_detected = [];
cascade_src = 'cas1.xml'
# Put the name of the image you want to process here
img_src = 'demo_2.jpg'
#video_src = 'dataset/video2.avi'

img = cv2.imread(img_src)
car_cascade = cv2.CascadeClassifier(cascade_src)
cv2.imshow('ImageWindow', img)
cv2.waitKey(0)

#while True:
#ret, img = cap.read()
if (type(img) == type(None)):
    exit()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cars = car_cascade.detectMultiScale(gray, 1.1, 1)

# Add the spots detected to the Image
for space in spaces:
    cv2.rectangle(img, (space['origin_x'], space['origin_y']), (space['origin_x']+SPOT_W, space['origin_y']+SPOT_H), (255,0,0),2)
for (x,y,w,h) in cars:
    if(w > 100 and h > 100):
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        centroidx = x+h/2
        centroidy = y+h/2
        newCar = {"cx": centroidx, "cy": centroidy, "w":w}
        cars_detected.append(newCar)
    #print("X Centroid is: %(x)d, Y Centroid is: %(y)d" % {'x': centroidx, 'y': centroidy})
# Now check to see if any of the cars fell in one of the spaces
numFilled = 0
for space in spaces:
    for car in cars_detected:
        if( (car['w'] >= 100) and (car['cx'] >= space['origin_x']) and (car['cx'] <= space['origin_x'] + SPOT_W) and (car['cy'] >= space['origin_y']) and (car['cy'] <= space['origin_y'] + SPOT_H)):
            print("Space %d is filled." % space['id'])
            print(car)
            numFilled += 1
# Tell how many spaces are empty
print("Number of Empty Spaces: %d" % (len(spaces) - numFilled))

cv2.imshow('DetectionWindow', img)
cv2.waitKey(0)
# If user presses esc, close window
if cv2.waitKey() == 27:
    cv2.destroyAllWindows()
