from math import pi, radians
import cv2, numpy as np
import skimage

class ViewWidget(object):

	# Should be rewritten
	def DrawRectangles(self, frame:list, circles:list, color:tuple=(0, 255, 0), thickness:int=1):
		if circles is not None:
			circles = np.uint16(np.around(circles))

			for (x, y, r) in circles[0,:]:

				cv2.rectangle(frame, (x-r, y-r), (x+r, y+r), color, thickness)

	def DrawCircles(self, frame:list, circles:list, color:tuple=(0, 255, 0), thickness:int=1):
		if circles is not None:
			circles = np.uint16(np.around(circles))

			for (x, y, r) in circles[0,:]:
				cv2.circle(frame, (x, y), r, color, thickness)

	def DrawCentroids(self, frame:list, circles:list, color:tuple=(0, 255, 0)):
		if circles is not None:
			circles = np.uint16(np.around(circles))

			for (x, y, r) in circles[0,:]:
				cv2.circle(frame, (x, y), 1, color, 2)

	def DrawObjectData(self, frame:list, data:dict, color:tuple=(0, 255, 0), font_size:float=0.7, thickness:int=1):
		if data is not None:
			for i in data:
				(x, y, r) = np.uint16(np.around(data[i]))
				cv2.putText(frame, f'{i}: {x}, {y}', (15, y), 0, font_size, color, thickness)

	# Base functions
	def DrawRectangle(self, frame:list, rect:tuple, color:tuple=(0, 255, 0), thickness:int=1):
		if len(rect) > 0:
			(x, y, w, h) = rect
			cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)

	def DrawText(self, frame:list, text:str, pos:tuple=(10, 30), color:tuple=(0, 0, 0), size:float=1, thickness:int=1):
		cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_PLAIN, size, color, thickness)

	def DrawCentroid(self, frame:list, pos:tuple, color:tuple=(0, 255, 0), size:int=1):
		cv2.circle(frame, pos, size, color, -1)

	def DrawHorizontalLine(self, frame:list, y:int, color:tuple=(0, 255, 255), thickness:int=1):
		(my, mx, mc) = np.shape(frame)
		cv2.line(frame, (0, y), (mx, y), color, thickness)

	def DrawVerticalLine(self, frame:list, x:int, color:tuple=(0, 255, 255), thickness:int=1):
		(my, mx, mc) = np.shape(frame)
		cv2.line(frame, (x, 0), (x, my), color, thickness)

	def DrawContours(self, frame:list, contours:list, color:tuple=(0, 0, 255), thickness:int=1):
		if len(contours[0]) > 0:
			cv2.drawContours(frame, contours, -1, color, thickness)
		
	# Base function combinations
	def DrawTrackingLimits(self, frame:list, y_start:int, y_end:int, color:tuple=(0, 255, 255), thickness:int=1):
		self.DrawHorizontalLine(frame, y_start, color, thickness)
		self.DrawHorizontalLine(frame, y_end, color, thickness)

	