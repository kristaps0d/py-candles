import cv2, numpy as np

# widgets
from widgets.counter.video import VideoWidget
from widgets.counter.mask import MaskWidget
from widgets.counter.track import TrackWidget, StatefulTrackingWidget
from widgets.counter.detect import DetectWidget
from widgets.counter.view import ViewWidget
from widgets.counter.markers import MarkerWidget

# detection pipelines
from widgets.counter.pipelines.white import WhitePipeline
from widgets.counter.pipelines.pink import PinkPipeline
from widgets.counter.pipelines.yellow import YellowPipeline

# correction pipelines
from widgets.counter.pipelines.circles import CorrectCicles
from widgets.counter.pipelines.defects import CheckDefectState, DefectDeltas

# handlers
from widgets.database.connection import DbConnection
from utils.exceptions import ExceptionHandler

class CounterModule(object):
	def __init__(self, video_source, dbUri):
		# Functional objects
		# self.capt = VideoWidget(video_source, 30 if type(video_source) is str else None)

		self.capt = VideoWidget(video_source, 30) ## DEBUG
		self.track = TrackWidget(90, 250)

		# Function objects
		self.detect = DetectWidget()
		self.mask = MaskWidget()
		self.draw = ViewWidget()
		self.mark = MarkerWidget()

		self.defective = StatefulTrackingWidget()
		self.defectStates = DefectDeltas()

		# Class public variables
		self.detection_upper_lim = 200

		# Class private variables
		self._dbUri = dbUri

		self.run()

	def run(self):
		self.capt.StartThread()

		with DbConnection(self._dbUri) as con:
			while True:

				# self.capt.ReadFrame()

				if self.capt.frame is not None:
					
					# user displays
					f_visuals, f_candles, f_markers = [self.capt.frame.copy()] * 3
					f_candles = self.mask.GuassianBlur(f_candles, (7, 7))
					
					# referance colorspaces
					rgb_ref = self.capt.frame.copy()
					hsv_ref = cv2.cvtColor(f_candles, cv2.COLOR_BGR2HSV)
					gray_ref = cv2.cvtColor(f_candles, cv2.COLOR_BGR2GRAY)

					# ArUco bounds detection
					rects, centroids, ids = self.detect.ArUcoMarkers(f_markers)
					bounds, points, center = self.mark.MarkerOuterBounds(centroids, ids)

					(h, w, d) = np.shape(hsv_ref)

					# 	masking off static glare, not implementing motion based filter
					#	dont have enough free time for such luxuries
					self.draw.DrawRectangle(hsv_ref, (0, 0, w, self.detection_upper_lim), (0, 0, 0), -1)
					
					sub_frame = f_candles[0:self.detection_upper_lim, 0:w]
					white_rect = np.ones_like(sub_frame, dtype=np.uint8)
					(r, g, b) = cv2.split(white_rect)
					# f_visuals[0:self.detection_upper_lim, 0:w] = cv2.addWeighted(sub_frame, 0.8, cv2.merge([r, g*255, b]), 0.1, 0.5)
					
					_white_mask = WhitePipeline(hsv_ref, gray_ref, self.mask)
					white_c = CorrectCicles(_white_mask, padding=5)
					
					_pink_mask = PinkPipeline(hsv_ref, gray_ref, self.mask)
					pink_c = CorrectCicles(_pink_mask)
					
					_yellow_mask = YellowPipeline(hsv_ref, gray_ref, self.mask)
					yellow_c = CorrectCicles(_yellow_mask)

					concat = [*white_c[0], *pink_c[0], *yellow_c[0]]

					defective_c = CheckDefectState(rgb_ref, concat, self.mask)
					self.defective.update(defective_c)
					self.defectStates.update(self.defective.known)

					for key in self.defective.known:
						(x, y, r, c) = np.int0(self.defective.known[key])
						_state = self.defectStates.states[key]
						state = 'bad' if _state > 1.6 else 'good'

						if state == 'bad':
							self.draw.DrawCircles(f_markers, [[[x, y, r]]], (0, 0, 255), 2)
						else:
							self.draw.DrawCircles(f_markers, [[[x, y, r]]], (0, 255, 0), 2)

						self.draw.DrawText(f_markers, f'{key} : {_state}', (x-30, y-50), (0, 255, 0), 1, 1)

					# display pipeline detections
					# self.draw.DrawCircles(f_visuals, [concat], (0, 0, 255), 1)
					# self.draw.DrawCircles(f_visuals, white_c, (0, 255, 0), 2)
					# self.draw.DrawCircles(f_visuals, pink_c, (255, 0, 0), 2)
					# self.draw.DrawCircles(f_visuals, yellow_c, (0, 0, 255), 2)





					# Display frames
					self.capt.ShowFrame(f_visuals, "visuals")
					self.capt.ShowFrame(hsv_ref, "hsv_ref")
					# self.capt.ShowFrame(f_markers, "Markers")

				if cv2.waitKey(25) & 0xFF == ord('q'):
					self.capt.StopThread()
					break

	def __del__(self):
		self.capt.StopThread()

class CounterModuleAsync(ExceptionHandler):
	def __init__(self, queue, video_source, dbUri):
		super().__init__()

		# Functional objects
		self.capt = VideoWidget(video_source, 30 if type(video_source) is str else None)
		self.track = TrackWidget(90, 250)

		# Function objects
		self.detect = DetectWidget()
		self.mask = MaskWidget()
		self.draw = ViewWidget()
		self.mark = MarkerWidget()

		# Class private variables
		self._dbUri = dbUri
		self._queue = queue

		self._show = {
			'visuals': False,
			'mask': False,
			'markers': False
		}

		self.run()

	def ResetDisplays(self):
		cv2.destroyAllWindows()

	def run(self):
		self.capt.StartThread()

		with DbConnection(self._dbUri) as con:
			while True:
				# self.capt.ReadFrame()
				try:
					_ret = self._queue.get(timeout=0)

					if _ret == 'visuals':
						self._show['visuals'] = not self._show['visuals']
						self.ResetDisplays()

					if _ret == 'mask':
						self._show['mask'] = not self._show['mask']
						self.ResetDisplays()

					if _ret == 'markers':
						self._show['markers'] = not self._show['markers']
						self.ResetDisplays()

				except:
					pass

				if self.capt.frame is not None:
					# Make copies of origional frame
					f_visuals, f_candles, f_markers = [self.capt.frame.copy()] * 3

					# f_candles detect process pipe
					f_candles = self.mask.Grayscale(f_candles)
					f_candles = self.mask.GuassianBlur(f_candles, (7, 7))
					thr = np.mean(f_candles) + (2 * np.std(f_candles))
					f_candles_thr = self.mask.Threshold(f_candles, thr)
					f_candles = cv2.bitwise_and(f_candles, f_candles, mask=f_candles_thr)
					f_candles = self.mask.GuassianBlur(f_candles, (9, 9))

					circles_thr = self.detect.HoughCircles(f_candles, dp=1, minRadius=25, maxRadius=50, minDist=20)

					f_candles_thr = np.zeros_like(f_candles)
					self.draw.DrawCircles(f_candles_thr, circles_thr, (255, 255, 255), -1)
					f_candles = cv2.bitwise_and(f_candles, f_candles, mask=f_candles_thr)

					# ArUco bounds detection
					rects, centroids, ids = self.detect.ArUcoMarkers(f_markers)
					bounds, points, center = self.mark.MarkerOuterBounds(centroids, ids)

					# 	bounds visualisation
					mask = np.zeros(f_markers.shape[:2], dtype="uint8")
					self.draw.DrawContours(mask, [bounds], (255, 255, 255), -1)
					f_markers = cv2.bitwise_and(f_candles, f_candles, mask=mask)
					

					# Draw visual data
					self.draw.DrawTrackingLimits(f_visuals, self.track.detection_threshold_start, self.track.tracking_threshold_end)
					self.draw.DrawText(f_visuals, str(len(self.track.delivered_objects)), size=0.8, pos=(5, self.track.detection_threshold_start+20), color=(0, 255, 0))

					# Circle detection
					circles = self.detect.HoughCircles(f_candles, dp=1, maxRadius=50, minDist=30)
					self.draw.DrawCircles(f_visuals, circles, (255, 0, 0), 1)

					# f_candles tracking pipe
					self.track.CentroidTracking(f_visuals, circles, con)
					self.draw.DrawCircles(f_visuals, [list(self.track.identified_objects.values())], (0, 180, 0), 2)

					self.draw.DrawRectangles(f_visuals, [list(self.track.identified_objects.values())], thickness=1)
					self.draw.DrawObjectData(f_visuals, self.track.identified_objects, (0, 0, 255), 1, 1)

					# Display frames
					if self._show['visuals']:
						self.capt.ShowFrame(f_visuals, "Application")

					if self._show['mask']:
						self.capt.ShowFrame(f_candles, "Candles")

					if self._show['markers']:
						self.capt.ShowFrame(f_markers, "Markers")

				if cv2.waitKey(25) & 0xFF == ord('q'):
					self.capt.StopThread()
					break

	def __del__(self):
		self.capt.StopThread()