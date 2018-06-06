# -*- coding: utf-8 -*-

# This is proof-of-concept code for the Mobi Parking Project
# adapted from GitHub User andrewssobral's haarcascades vehicle detection program
# Last Edit: 6/3/2018 by Ross Hartley

import cv2
print(cv2.__version__)

SPOT_W = 126
SPOT_H = 255
spaces = [{"origin_x": 190, "origin_y": 45, "id": 0},
    {"origin_x": 316, "origin_y": 45, "id": 1},
    {"origin_x": 442, "origin_y": 45, "id": 2},
    {"origin_x": 568, "origin_y": 45, "id": 3},
    {"origin_x": 694, "origin_y": 45, "id": 4},
    {"origin_x": 820, "origin_y": 45, "id": 5},
    {"origin_x": 946, "origin_y": 45, "id": 6},
    {"origin_x": 190, "origin_y": 335, "id": 7},
    {"origin_x": 316, "origin_y": 335, "id": 8},
    {"origin_x": 442, "origin_y": 335, "id": 9},
    {"origin_x": 568, "origin_y": 335, "id": 10},
    {"origin_x": 694, "origin_y": 335, "id": 11},
    {"origin_x": 820, "origin_y": 335, "id": 12},
    {"origin_x": 946, "origin_y": 335, "id": 13}]
cars_detected = [];
cascade_src = 'cars.xml'
# Put the name of the image you want to process here
img_src = 'half_full.jpg'
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

for (x,y,w,h) in cars:
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
    centroidx = x+h/2
    centroidy = y+h/2
    newCar = {"cx": centroidx, "cy": centroidy}
    cars_detected.append(newCar)
    print("X Centroid is: %(x)d, Y Centroid is: %(y)d" % {'x': centroidx, 'y': centroidy})
# Now check to see if any of the cars fell in one of the spaces
numFilled = 0
for space in spaces:
    for car in cars_detected:
        #print(car)
        if( (car['cx'] >= space['origin_x']) and (car['cx'] <= space['origin_x'] + SPOT_W) and (car['cy'] >= space['origin_y']) and (car['cy'] <= space['origin_y'] + SPOT_H)):
            print("Space %d is filled." % space['id'])
            numFilled += 1
# Tell how many spaces are empty
print("Number of Empty Spaces: %d" % (14 - numFilled))

cv2.imshow('DetectionWindow', img)
cv2.waitKey(0)
# If user presses esc, close window
if cv2.waitKey() == 27:
    cv2.destroyAllWindows()
