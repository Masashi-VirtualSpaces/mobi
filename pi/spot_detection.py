'''
    This program detects the location of spaces in the parking lot
    Written on 6/23/2018 by Ross Hartley
'''

import cv2
import numpy as np
import csv
from matplotlib import pyplot as plt

def saveData(width, height, points):
    with open('data.csv', 'w') as myfile:
        writer = csv.writer(myfile)
        writer.writerow(['Width'] + [width])
        writer.writerow(['Height'] + [height])
        for point in points:
            writer.writerow([point['x'], point['y']])
    print('Data successfully written to data.csv')

def findIntersections(vert_lines, hori_lines):
    points = []
    for vline in vert_lines:
        for hline in hori_lines:
            if(hline[1] > np.amin([vline[1], vline[3]]) and hline[1] < np.amax([vline[1], vline[3]])):
                if(vline[0] > np.amin([hline[0], hline[2]]) and vline[0] < np.amax([hline[0], hline[2]])):
                    points.append({'x': vline[0],'y': hline[1]})
    return points

def filterPoints(points):
    sortedlist = sorted(points, key=lambda k: k['x'])
    newlist = []
    for i in range(1, len(sortedlist)):
        if(abs(sortedlist[i]['x']-sortedlist[i-1]['x']) > 25):
            newlist.append(sortedlist[i-1])
    return newlist

def getWidth(points):
    distance = []
    for i in range(1, len(points)):
        distance.append(abs(points[i]['x']-points[i-1]['x']))
    return int(np.average(distance))

def getHeight(vert_lines):
    height = []
    for line in vert_lines:
        height.append(abs(line[1] - line[3]))
    return int(np.average(height))

print(cv2.__version__)

img_src = 'demo.jpg'

img = cv2.imread(img_src)
brightness = 0
contrast = 127
adj = cv2.addWeighted(img, 1.0 + contrast/127.0, img, 0, brightness - contrast)
lower = np.uint8([150, 150, 150])
upper = np.uint8([255, 255, 255])
mask = cv2.inRange(adj, lower, upper)
#edgy = cv2.Canny(mask,20,20)

rho = 10  # distance resolution in pixels of the Hough grid
theta = np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 15  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 175  # minimum number of pixels making up a line
max_line_gap = 10  # maximum gap in pixels between connectable line segments

# Run Hough on masked image
# Output "lines" is an array containing endpoints of detected line segments
lines = cv2.HoughLinesP(mask, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)
line_img = img
vert_lines = []
hori_lines = []
for line in lines:
    for x1,y1,x2,y2 in line:
        # Only want lines that are mostly vertical
        if(np.abs(x1-x2) < 15):
            cv2.line(line_img,(x1,y1),(x2,y2),(255,0,0),5)
            vert_lines.append([x1,y1,x2,y2])
            continue
        # Or horizontal
        if(np.abs(y1-y2) < 25):
            cv2.line(line_img,(x1,y1),(x2,y2),(0,255,0),5)
            hori_lines.append([x1,y1,x2,y2])
            continue
print('Vertical Lines: ')
print(vert_lines)
print('Horizontal Lines: ')
print(hori_lines)
cv2.imshow('Image', line_img)
cv2.waitKey(0)
# Do a second mask to get an image of only identified lines
nlower = np.uint8([250, 0, 0])
nupper = np.uint8([255, 0, 0])
mask2 = cv2.inRange(line_img, nlower, nupper)
# find points where vertical and horizontal lines intersect
points = findIntersections(vert_lines, hori_lines)
points = filterPoints(points)
print(points)
width = getWidth(points)
height = getHeight(vert_lines)

for point in points:
        # We know the spots are directly accros from each other so draw two rectangles
        cv2.rectangle(img,(point['x'],point['y']),(point['x'] + width,point['y'] + height),(0,0,255),4)
        cv2.rectangle(img,(point['x'],point['y']),(point['x'] + width,point['y'] - height),(0,0,255),4)

width = getWidth(points)
height = getHeight(vert_lines)

print('Width: %d'% width)
print('Height: %d'% height)
saveData(width, height, points)

cv2.imwrite('results.jpg', line_img)

plt.subplot(161),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(162),plt.imshow(adj,cmap = 'gray')
plt.title('Adjusted Image'), plt.xticks([]), plt.yticks([])
plt.subplot(163),plt.imshow(mask,cmap = 'gray')
plt.title('Masked Image'), plt.xticks([]), plt.yticks([])
plt.subplot(164),plt.imshow(mask2,cmap = 'gray')
plt.title('New Image'), plt.xticks([]), plt.yticks([])
#plt.subplot(165),plt.imshow(edgy,cmap = 'gray')
#plt.title('Edgy'), plt.xticks([]), plt.yticks([])
plt.subplot(166),plt.imshow(img,cmap = 'gray')
plt.title('Final'), plt.xticks([]), plt.yticks([])
plt.show()
