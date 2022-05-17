import cv2, numpy as np
import math, time

class TrackWidget(object):
	def __init__(self, y_track_height, y_offset:int=30):

		# Centroid tracking
		self.tracking_threshold_end = y_offset
		self.detection_threshold_start = y_track_height + y_offset

		self.current_objects, self.delivered_objects = {}, {}
		self.circles, self.current_id = [], 0


	# Centroid tracking
	def GetCircles(self, circles:list):
		if circles is None:
			return None

		for (x, y, r) in circles[0,:]:
			if y < self.detection_threshold_start:
				self.circles.append((x, y, r))

		return self.circles

	def CentroidTracking(self, frame:list, circles:list):
		if circles is None:
			return 

		self.GetCircles(circles)

		if len(self.circles) > 0:
			for i in list(self.current_objects):
				(x, y, r) = self.current_objects[i]

				# Know point tracking end point
				if y < self.tracking_threshold_end:
					self.delivered_objects[i] = self.current_objects.pop(i)
					pass
				
				# Known point comparison, tracking
				for j, (cx, cy, cr) in enumerate(self.circles):
					dx, dy = abs(x-cx), abs(y-cy)
					distance = math.sqrt(dx*dx + dy*dy)

					if distance <= r * 1:
						# New known point position
						if cy > self.tracking_threshold_end:
							self.current_objects[i] = (cx, cy, cr)
						else:
							# Uses 'Known point tracking end point' to delete
							self.current_objects[i] = (0, 0, 0)		

						self.circles.pop(j)
						break

			# New point detection, registration
			for i, (x, y, r) in enumerate(self.circles):
				if y > self.tracking_threshold_end:
					self.current_objects[self.current_id] = (x, y, r)
					self.current_id += 1

				self.circles.pop(i)

			print(f'Visible: {len(self.current_objects)}, Delivered: {len(self.delivered_objects)}, Seen: {self.current_id}')
			
			