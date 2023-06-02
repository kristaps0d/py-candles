import cv2, numpy as np

class WhitePipeline(object):
    def __new__(self, hsv_ref, gray_ref, mask_handle, l_bounds:list=[0, 0, 180], u_bounds:list=[50, 100, 255], thr_multiplier=2):

        # color segmentation
        l_bounds, u_bounds = np.array(l_bounds), np.array(u_bounds)
        mask_ref = cv2.inRange(hsv_ref, l_bounds, u_bounds)
        gray_ref = cv2.bitwise_and(gray_ref, gray_ref, mask=mask_ref)

        gray_ref = cv2.filter2D(src=gray_ref, ddepth=-1, kernel=np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]))        

        # gray_ref = cv2.erode(gray_ref, np.ones((3, 3)), iterations=5)
        gray_ref = mask_handle.GuassianBlur(gray_ref, (3, 3)) 
        gray_ref = mask_handle.Threshold(gray_ref, np.mean(gray_ref)+1*np.std(gray_ref))

        return gray_ref