#!/usr/bin/env python

import cv2
# from opencvutils.video import Camera


cam = cv2.VideoCapture(0)
# cam.init(cameraNumber=0, win=(640, 480))

while True:
	try:
		ret, img = cam.read()
		cv2.imshow('img', img)
		if cv2.waitKey(1) == 27:
			break  # esc to quit

	except:
		# cam.close()
		break

cv2.destroyAllWindows()
print('bye ...')
