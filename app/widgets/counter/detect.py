import cv2, numpy as np
import cv2.aruco as aruco
import math, time

class DetectWidget(object):
	def HoughCircles(self, frame:list, method:int=cv2.HOUGH_GRADIENT, dp:int=1, minDist:float=20, cannyt:float=20, centt:float=20, minRadius:int=0, maxRadius:int=0) -> list:
		return cv2.HoughCircles(frame, method, dp, minDist, param1=cannyt, param2=centt, minRadius=minRadius, maxRadius=maxRadius)

	def ArUcoMarkers(self, frame:list, dict_type:any=aruco.DICT_ARUCO_ORIGINAL):

		# General detection
		arucoDict = aruco.Dictionary_get(dict_type)
		arucoParm = aruco.DetectorParameters_create()

		contours, ids, inv = aruco.detectMarkers(frame, arucoDict, parameters=arucoParm)

		# Data parsing
		bounds, centroids = [], []

		if contours != ():
			for contour in contours:
				rect = cv2.boundingRect(contour)

				(x, y, w, h) = rect
				c_x, c_y = int(x + (w / 2)), int(y + (h / 2))

				bounds.append(rect)
				centroids.append((c_x, c_y))

		if ids is None:
			ids = []

		return bounds, centroids, ids