import cv2, numpy as np
import cv2.aruco as aruco
import math, time

class DetectWidget(object):
	def HoughCircles(self, frame:list, method:int=cv2.HOUGH_GRADIENT, dp:int=1, minDist:float=20, cannyt:float=20, centt:float=20, minRadius:int=0, maxRadius:int=0) -> list:
		return cv2.HoughCircles(frame, method, dp, minDist, param1=cannyt, param2=centt, minRadius=minRadius, maxRadius=maxRadius)

	def ArUcoMarkers(self, frame:list, marker_size:int=6, total_markers:int=250):
		arucoDict = aruco.Dictionary_get(getattr(aruco, f'DICT_{marker_size}X{marker_size}_{total_markers}'))
		arucoParm = aruco.DetectorParameters_create()

		contours, ids, inv = aruco.detectMarkers(frame, arucoDict, parameters=arucoParm)
		markers = []

		if len(contours) > 0:
			for i, (corner, id) in enumerate(zip(contours[0], ids[0])):
				(t_left, t_right, b_right, b_left) = corner
				cx, cy = int(t_left[0] + b_left / 2), int(t_left[1] + b_right[1] / 2)
				# markers.append((cx, cy, 5))

		return markers

		# return (r_contours, r_ids)