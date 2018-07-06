import cv2
import boto3
import dynamo_worker
# -*- coding: utf-8 -*-

# This is proof-of-concept code for the Mobi Parking Project
# adapted from GitHub User andrewssobral's haarcascades vehicle detection program
# Last Edit: 7/6/2018 by Ross Hartley

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
	
def vehicle_detection():
	print(cv2.__version__)

	SPOT_W, SPOT_H, spaces = getData()
	cascade_src = 'cars.xml'
	# Put the name of the image you want to process here
	img_src = '/tmp/parkinglot.jpg'
	#video_src = 'dataset/video2.avi'

	img = cv2.imread(img_src)
	car_cascade = cv2.CascadeClassifier(cascade_src)
	#cv2.imshow('ImageWindow', img)
	#cv2.waitKey(0)

	#while True:
	#ret, img = cap.read()
	if (type(img) == type(None)):
		print("Image not found. Exiting...")
		exit()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	cars = car_cascade.detectMultiScale(gray, 1.1, 1)

	for (x,y,w,h) in cars:
		#cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
		centroidx = x+h/2
		centroidy = y+h/2
		newCar = {"cx": centroidx, "cy": centroidy, "w":w}
		cars_detected.append(newCar)
		print("X Centroid is: %(x)d, Y Centroid is: %(y)d" % {'x': centroidx, 'y': centroidy})
	# Now check to see if any of the cars fell in one of the spaces
	numFilled = 0
	for space in spaces:
		for car in cars_detected:
			#print(car)
			if( (car['w'] >= 100) and (car['cx'] >= space['origin_x']) and (car['cx'] <= space['origin_x'] + SPOT_W) and (car['cy'] >= space['origin_y']) and (car['cy'] <= space['origin_y'] + SPOT_H)):
				print("Space %d is filled." % space['id'])
				numFilled += 1
	# Tell how many spaces are empty
	print("Number of Empty Spaces: %d" % (10 - numFilled))

	#cv2.imshow('DetectionWindow', img)
	#cv2.waitKey(0)
	# If user presses esc, close window
	#if cv2.waitKey() == 27:
	#   cv2.destroyAllWindows()
	# returning number of empty spaces
	return (10-numFilled)

def lambda_handler(event, context):
	print("OpenCV installed version:", cv2.__version__)

	s3 = boto3.resource('s3')
	dw = dynamo_worker.dynamo_worker()
	if event:
		print('Event :', event)
		file_obj = event["Records"][0]
		filename = str(file_obj ['s3']['object']['key'])
		print("Filename : ",filename)
		#What does the key represent??? and how could it be used?

		#file_obj = s3.get_object(Bucket = "mobiparking2", Key = filename)
		#file_obj.download_file('parkinglot.jpg')
		s3.Object('testlot1527031324.846385', filename).download_file('/tmp/parkinglot.jpg')
		#print("File Obj : ", file_obj)
		#file_content = file_obj["Body"].read().decode("utf-8")
		#print(file_content)
		openSpaces = vehicle_detection()
		taken = 10-openSpaces
		dw.updateItem(taken, openSpaces)
	return "It works!"

if __name__ == "__main__":
	lambda_handler(42, 42)
