import cv2, numpy as np
from widgets import VideoWidget, MaskWidget, TrackWidget, DetectWidget, ViewWidget, MarkerWidget

class CounterModule(object):
	def __init__(self, video_source):
		# Functional objects
		self.capt = VideoWidget(video_source, 30 if type(video_source) is str else None)
		self.track = TrackWidget(200, 80)

		# Function objects
		self.detect = DetectWidget()
		self.mask = MaskWidget()
		self.draw = ViewWidget()
		self.mark = MarkerWidget()

	def run(self):
		# self.capt.StartThread()

		while True:
			self.capt.ReadFrame()

			if self.capt.frame is not None:
				# Make copies of origional frame
				f_visuals, f_candles, f_markers = self.capt.frame.copy(), self.capt.frame.copy(), self.capt.frame.copy()

				# Apply mask to frame
				f_candles = self.mask.CandleMask(f_candles)



				# TO BE REWRITTEN JUST EXPERIMENTAL CODE
				rects, centroids, ids = self.detect.ArUcoMarkers(f_markers)
				bounds, points, center = self.mark.MarkerOuterBounds(centroids, ids) #, [10, 14, 37, 41, 9, 3, 2]

				for i in points:
					cv2.circle(f_markers, i, 10, (0, 255, 0), -1)

				mask = np.zeros(f_markers.shape[:2], dtype="uint8")
				self.draw.DrawContours(mask, [bounds], (255, 255, 255), -1)

				f_markers = cv2.bitwise_and(f_markers, f_markers, mask=mask)

				if len(center) > 0:
					cv2.circle(f_markers, center, 2, (0, 0, 255), -1)
				
				# TO BE REWRITTEN JUST EXPERIMENTAL CODE




				# Draw visual data
				self.draw.DrawTrackingLimits(f_visuals, self.track.detection_threshold_start, self.track.tracking_threshold_end)
				self.draw.DrawText(f_visuals, str(self.track.current_id), size=0.8, pos=(5, self.track.detection_threshold_start+20), color=(0, 255, 0))

				# Run circle detection, display with blue circles
				circles = self.detect.HoughCircles(f_candles, dp=1, maxRadius=50, minDist=30)
				self.draw.DrawCircles(f_visuals, circles, (255, 0, 0), 1)

				# Run object tracking
				self.track.CentroidTracking(f_candles, circles)
				self.draw.DrawRectangles(f_visuals, [list(self.track.current_objects.values())], thickness=1)
				self.draw.DrawObjectData(f_visuals, self.track.current_objects, (0, 255, 0), 0.3, 1)

				# Display frames
				self.capt.ShowFrame(f_visuals, "Application")
				self.capt.ShowFrame(f_candles, "Candles")
				self.capt.ShowFrame(f_markers, "Markers")

			if cv2.waitKey(25) & 0xFF == ord('q'):
				self.capt.StopThread()
				break

	def __del__(self):
		self.capt.StopThread()