import cv2, numpy as np
import math, time

from widgets.counter.events.delivered import LegacyDeliveredEvent
from widgets.counter.events.log import LogEvent

class StatefulTrackingWidget(object):
    def __init__(self):

        self.report = []

        self.known = {}
        self.new = []

        self.id = 0
        self.max_dev = 1.5
        self.min_radius = 25

    def newId(self):
        self.id += 1
        return self.id

    def parseNew(self, report):
        # submit new items to processing pipe
        for (x, y, r, c) in report:

            if (r < self.min_radius):
                continue

            self.new.append([x, y, r, c])

    def update(self, defective_report:list, precentage:float=0):
        
        self.parseNew(defective_report)
        
        if (len(self.new) == 0):
            return

        fullfilled = {}

        for key in list(self.known.keys()):
            (x, y, r, c) = self.known[key]
            _check_delta = x + y + r

            _dist, _index = None, None
            for _key, (_x, _y, _r, _c) in enumerate(self.new):

                
                _dy = _y - y
                _dx = abs(_x - x)

                _tmp_dist = -1 * _dy * _dx

                # cant go reverse only forwards
                if (_tmp_dist < 0):
                    continue

                if (_index) and (_dist < _tmp_dist):
                    continue
                
                _dist, _index = _tmp_dist, _key

            if (_index == None):
                self.known.pop(key)
				# Count as delivered
                DeliveredEvent(key)
                continue

            if (_dist > r * self.max_dev):    
                continue
            
            self.known[key] = self.new.pop(_key)
            fullfilled[key] = True

        for key in list(self.known.keys()):
            if key not in fullfilled:
                self.known.pop(key)

        for _key, obj in enumerate(self.new):
            obj = self.new.pop(_key)
            self.known[self.newId()] = obj

class TrackWidget(object):
	def __init__(self, y_track_height, y_offset:int=30, max_history_ref_size:int=10):

		# class static variables
		self.tracking_threshold_end = y_track_height + y_offset
		self.detection_threshold_start = y_offset

		# private class variables
		
		# Object tracking stages
		self.detected_objects = []

		self.identified_objects = {}
		self.identified_object_histories = {}

		self.id = 0
		self._hist_max_len = max_history_ref_size

		self.delivered_objects = {}

		self.predicted_objects = {}
	
	def GetNewId(self):
		self.id += 1
		return self.id

	# Centroid tracking
	def GetDetected(self, circles:np.array):
		if circles is None:
			return None

		_entities = list(circles[0,:])

		for (x, y, r) in _entities:
			self.detected_objects.append((x, y, r))

		return self.detected_objects

	def AddHistoryDatapoint(self, id, datapoint):

		if id not in self.identified_object_histories:
			self.identified_object_histories[id] = []

		_delta = len(self.identified_object_histories[id]) - self._hist_max_len

		if _delta > 0:
			self.identified_object_histories[id] = self.identified_object_histories[id][_delta:]

		self.identified_object_histories[id].append(datapoint)

	def CentroidTracking(self, frame:list, circles:list, dbCon):
		
		if circles is None:
			return 

		self.GetDetected(circles)

		if len(self.detected_objects) > 0:
			fullfilled = {}

			for i in list(self.identified_objects):
				(x, y, r) = self.identified_objects[i]

				# Endpoint comparison
				if y > self.tracking_threshold_end:
					_obj = self.identified_objects.pop(i)
					_obj_quality = 'passed'

					self.delivered_objects[i] = _obj
					_ret = LegacyDeliveredEvent(_obj, _obj_quality, dbCon)
					continue
				
				# check for possible nearest new position
				_dist, _index = None, None
				for _i, (_cx, _cy, _cr) in enumerate(self.detected_objects):

					_dx, _dy, _dr = abs(x - _cx), abs(y - _cy), abs(r - _cr)
					_tmp_dist = math.sqrt(_dx*_dx + _dy*_dy)
					
					if _dist is not None:
						if _dist < _tmp_dist:
							continue

					_dist = _tmp_dist
					_index = _i

				# break case no new position
				if _index is None:
					self.identified_objects.pop(i)
					
					if i in self.identified_object_histories:
						self.identified_object_histories.pop(i)
					
					continue

				if _dist > r * 1.5:
					self.detected_objects.pop(_index)
					continue
					
				# update new position
				_datapoint = self.detected_objects.pop(_index)
				
				self.identified_objects[i] = _datapoint
				self.AddHistoryDatapoint(i, _datapoint)

				fullfilled[i] = True

			# destroy unfulfilled contracts
			for i in list(self.identified_objects):
				if i not in fullfilled:

					print(f'info: phantom detection corrected [id]: {i}')
					LogEvent(f'info: phantom detection corrected [id]: {i}', dbCon)

					self.identified_objects.pop(i)

			# try to identify objects for future
			for i, (x, y, r) in enumerate(self.detected_objects):
				
				if y > self.detection_threshold_start and y < self.tracking_threshold_end:
					self.identified_objects[f'{self.GetNewId()}'] = (x, y, r)

				self.detected_objects.pop(i)
			