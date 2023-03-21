import cv2, time, numpy as np
import threading as thr

class VideoWidget(object):
	def __init__(self, src, fps_limit:int=None):
		# Main capture object
		self.capture = cv2.VideoCapture(src)
		
		# Predefined class variables
		self.ret, self.frame,  = None, None
		self.end_flag, self.fps_limit = False, fps_limit

		# Class video capture threading
		self.thread = thr.Thread(target=self.Update)

	def Update(self) -> None:
		while True:
			# Subroutine conditional break
			if self.end_flag is True:
				break
		
			if self.ret is False:
				break

			self.ReadFrame()

			if self.fps_limit is not None:
				time.sleep(1 / self.fps_limit)

	def ReadFrame(self):
		self.ret, self.frame = self.capture.read()

	def ShowFrame(self, frame:list, identifier:str="") -> None:
		cv2.imshow(identifier, frame)

	def StartThread(self):
		self.thread.start()

	def StopThread(self):
		self.end_flag = True