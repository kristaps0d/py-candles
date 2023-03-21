import cv2, numpy as np

class PinkPipeline(object):
    def __new__(self, hsv_ref, gray_ref, mask_handle, l_bounds:list=[80, 110, 0], u_bounds:list=[215, 255, 255], thr_min=50, thr_multiplier=1):

        # color segmentation
        l_bounds, u_bounds = np.array(l_bounds), np.array(u_bounds)
        _color_mask = cv2.inRange(hsv_ref, l_bounds, u_bounds)

        gray_ref = cv2.bitwise_and(gray_ref, gray_ref, mask=_color_mask)
        
        # thr: relu( mean + std, min )
        thr = max(np.mean(gray_ref) + (thr_multiplier * np.std(gray_ref)), thr_min)

        _mask = mask_handle.Threshold(gray_ref, thr)
        white = np.ones_like(gray_ref) * 255
        gray_ref = cv2.bitwise_and(white, white, mask=_mask)

        return gray_ref