import cv2, numpy as np

class CorrectCicles(object):
    def __new__(self, mask_ref, padding:float=0):
        
        contours, hierarchy = cv2.findContours(mask_ref, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        circles = []

        for c in contours:
            
            area = cv2.contourArea(c)

            # removing small features
            if area < 500:
                continue

            M = cv2.moments(c)

            # removing invalid contours
            if (not M["m10"] or not M["m00"] or not M["m01"]):
                continue

            # center determination
            cx, cy = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            theta = 0.5*np.arctan2(2*M["mu11"],M["mu20"]-M["mu02"])

            ((cx, cy), r) = cv2.minEnclosingCircle(c)           

            circles.append([cx, cy, r + padding])

        return [circles]