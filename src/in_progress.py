"""
TODO: Docstring

Author: @SamuelDubos
Date: January 24, 2024
"""

import numpy as np
import cv2


class PixelTracker:

    def __init__(self, camera):
        self.camera = camera

        self.point_selected = False
        self.point = None
        self.frames = []

        self.cap = cv2.VideoCapture(self.camera)
        cv2.namedWindow('Frame')
        cv2.setMouseCallback('Frame', self.select_point)
        self.lk_params = dict(winSize=(15, 15),
                              maxLevel=2,
                              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    def select_point(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.point_selected = True
            self.point = np.array([[x, y]], dtype=np.float32)

    def main(self):
        while True:
            _, frame = self.cap.read()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if self.point_selected:
                new_point, status, error = cv2.calcOpticalFlowPyrLK(self.frames[0],
                                                                    gray_frame,
                                                                    self.point,
                                                                    None,
                                                                    **self.lk_params)
                good_new = new_point[status.flatten() == 1]
                good_old = self.point[status.flatten() == 1]
                for new, old in zip(good_new, good_old):
                    a, b = new.ravel()
                    c, d = old.ravel()
                    frame = cv2.line(frame, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 2)
                    frame = cv2.circle(frame, (int(a), int(b)), 5, (0, 255, 0), -1)
                    frame = cv2.circle(frame, (int(c), int(d)), 5, (0, 0, 255), -1)
            self.frames.append(gray_frame.copy())
            cv2.imshow('Frame', frame)
            key = cv2.waitKey(1) & 0xFF
            if key in [ord('q')]:
                break
        cv2.destroyAllWindows()


if __name__ == '__main__':
    tracker = PixelTracker(0)
    tracker.main()
