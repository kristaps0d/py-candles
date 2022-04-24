import cv2, numpy as np

class MaskWidget(object):

	def CropFrame(self, frame:list, corner1:tuple, corner2:tuple) -> list:
		(x1, y1), (x2, y2) = corner1, corner2

		r_frame = frame[y1:y2, x1:x2]
		return r_frame

	def Grayscale(self, frame:list) -> list:
		return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	def GuassianBlur(self, frame:list, ksize:tuple=(5, 5), borderType:int=cv2.BORDER_CONSTANT) -> list:
		return cv2.GaussianBlur(frame, ksize, borderType)

	def Threshold(self, frame:list, thresh:int=127, maxval:int=255, type:int=cv2.THRESH_BINARY) -> list:
		ret, thresh = cv2.threshold(frame, thresh, maxval, type)
		return thresh

	def MaskBase(self, frame:list) -> list:
		r_frame = self.Grayscale(frame)
		r_frame = self.GuassianBlur(r_frame)
		return r_frame

	def CandleMask(self, frame:list) -> list:
		r_frame = self.MaskBase(frame)
		mask = self.Threshold(r_frame, 200, 255)

		r_frame = cv2.bitwise_and(r_frame, r_frame, mask=mask)

		r_frame = self.GuassianBlur(r_frame, (5, 5), cv2.BORDER_ISOLATED)

		mask = self.Threshold(r_frame, 200, 255)
		r_frame = self.GuassianBlur(mask, (5, 5), cv2.BORDER_ISOLATED)
		return r_frame

	def MarkerMask(self, frame:list, lower:int=120, upper:int=255) -> list:
		r_frame = self.Grayscale(frame)
		r_frame = self.Threshold(r_frame, lower, upper, cv2.THRESH_BINARY_INV)
		# r_frame = self.GuassianBlur(r_frame, (5, 5))
		return r_frame

	def EmptyClearCaseMask() -> list:
		# inRange instead of threshold
		pass

	def EmptyMetalCaseMask() -> list:
		# inRange instead of threshold
		pass
