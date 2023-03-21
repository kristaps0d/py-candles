import cv2, numpy as np

class CheckDefectState(object):
    def __new__(self, rgb_ref, circles, mask_handle, padding:int=5):

        ret = []
        for i, (x, y, r) in enumerate(np.int0(circles[0:])):
            r += padding
            crop = rgb_ref[y-r:y+r, x-r:x+r]
            crop_mask = mask_handle.GuassianBlur(crop, (7, 7))

            # crop_mask thresholding
            thr = np.mean(crop_mask)
            crop_mask = mask_handle.Threshold(crop_mask, thr)
            crop_mask = mask_handle.Grayscale(crop_mask)
            crop_mask = cv2.bitwise_and(crop, crop, mask=crop_mask)

            # high sensitivity edge detection using sobel kernels (right, left, bottom)
            r_sobl_mask = cv2.filter2D(src=crop_mask, ddepth=-1, kernel=np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]))
            l_sobl_mask = cv2.filter2D(src=crop_mask, ddepth=-1, kernel=np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]))
            b_sobl_mask = cv2.filter2D(src=crop_mask, ddepth=-1, kernel=np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]]))
            t_sobl_mask = cv2.filter2D(src=crop_mask, ddepth=-1, kernel=np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]))
            mask = r_sobl_mask + l_sobl_mask + b_sobl_mask + t_sobl_mask

            # mask = cv2.dilate(mask, np.ones((3, 3)), iterations=2)
            mask = mask_handle.GuassianBlur(mask, (7, 7))
            mask = mask_handle.Threshold(mask, np.mean(mask), 255)

            blank_ref = np.zeros_like(rgb_ref)
            blank_ref[y-r:y+r, x-r:x+r] = mask
            mask = mask_handle.Grayscale(blank_ref)  

            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            children = [c for c in contours[1:] if cv2.contourArea(c) > 180]

            # # debugging
            # mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
            # cv2.putText(mask, f'{len(children)}', (50, 50), 0, 1, (0, 255, 0), 1)

            # mask = cv2.drawContours(mask, [contours[0]], -1, (0, 255, 0), 1)            
            # mask = cv2.drawContours(mask, children, -1, (0, 0, 255), -1)

            # cv2.imshow(f'{i}', mask)

            ret.append([x, y, r, len(children)])

        return ret

class DefectDeltas(object):
    def __init__(self):
        self.history = {}
        self.states = {}

    def update(self, known):
        
        for key in known:
            (x, y, r, c) = known[key]

            if key not in self.history:
                self.history[key] = [c]
                self.states[key] = c
                continue
        
            self.history[key].append(c)
            self.states[key] = np.mean(self.history[key])

        return self.states
