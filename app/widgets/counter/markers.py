import cv2, math, numpy as np

class MarkerWidget(object):
	def __init__(self, max_frame_resize:float=0.2):
		# Class variables
		self.bounds = []
		self.thresh = max_frame_resize

	def Angle(self, x:float, y:float) -> tuple:
		return np.rad2deg(np.arctan2(y, x))

	def Quadrant(self, center:tuple, point:tuple) -> int:
		(c_x, c_y), (x, y) = center, point

		if x > c_x and y > c_y:
			return 1
		elif x < c_x and y > c_y:
			return 2
		elif x < c_x and y < c_y:
			return 3
		elif x > c_x and y < c_y:
			return 4
		else:
			return 0

	def BoundsBoundingBox(self, corners):
		bounds = cv2.boundingRect(np.int0(corners))
		return bounds

	def BoundsMinArea(self, corners):
		rect = cv2.minAreaRect(np.int0(corners))
		bounds = np.int0(cv2.boxPoints(rect))
		return bounds

	def MarkerOuterBounds(self, centroids:list, ids:list, whitelist_ids:tuple=None):
		points, quadrants = [], {1:[], 2:[], 3:[], 4:[]}

		# List filter pass
		if whitelist_ids is not None:
			for i, id in enumerate(ids):
				for w_id in whitelist_ids:
					if id == w_id:
						points.append(centroids[i])
						pass
		else:
			points = centroids

		if len(points) > 0:
			# Calculate center of filtered points
			c_x, c_y = sum([x for (x, y) in points]) / max(len(points), 1), sum([y for (x, y) in points]) / max(len(points), 1)

			# Sort points array by angles
			polar = np.array([self.Angle(x - c_x, y - c_y) for (x, y) in points])		
			points = np.array(points)[polar.argsort()[::-1]]


			# Divide points by quadrants
			for point in points:
				q = self.Quadrant((c_x, c_y), point)
				if q > 0:
					quadrants[q].append(point)

			for q in quadrants:
				max_dist, max_point = 0, None

				for (x, y) in quadrants[q]:
					dist = math.sqrt((x - c_x)**2 + (y - c_y)**2)

					if dist > max_dist:
						max_dist = dist
						max_point = [x, y]

				if max_dist > 0:
					quadrants[q] = max_point

			corners = list(quadrants.values())

			# Find outer bounds
			if len(corners[0]) > 0 and len(corners[1]) > 0 and len(corners[2]) > 0 and len(corners[3]) > 0:
				self.bounds = np.int0(corners)
			else:
				return [], [], []
 
			return self.bounds, corners, (int(c_x), int(c_y))
		return [], [], []