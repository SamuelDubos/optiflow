"""
TODO: Docstring

Author: @SamuelDubos
Date: January 24, 2024
"""

import numpy as np
import cv2


class PoiTracker:

    def __init__(self, camera, num_points):
        self.camera = camera
        self.num_points = num_points
        self.rect_start = None
        self.rect_end = None
        self.selecting_rect = False
        self.tracking_points = None
        self.prev_img = None

        self.cap = cv2.VideoCapture(self.camera, cv2.CAP_DSHOW)
        cv2.namedWindow('Frame')
        cv2.setMouseCallback('Frame', self.select_rect)
        self.lk_params = dict(winSize=(15, 15),
                              maxLevel=2,
                              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    def select_rect(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if not self.selecting_rect:
                print(f'Zone begins {x, y}')
                self.rect_end = None
                self.rect_start = (x, y)
                self.selecting_rect = True
            else:
                print(f'Zone ends {x, y}')
                self.rect_end = (x, y)
                self.selecting_rect = False
                _, frame = self.cap.read()
                self.tracking_points = self.generate_poi(frame)

    def generate_poi(self, frame):
        if self.rect_start is not None and self.rect_end is not None:
            x_min, y_min = np.min([self.rect_start, self.rect_end], axis=0).ravel()
            x_max, y_max = np.max([self.rect_start, self.rect_end], axis=0).ravel()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners = cv2.goodFeaturesToTrack(gray_frame[y_min:y_max, x_min:x_max],
                                              maxCorners=self.num_points, qualityLevel=0.01, minDistance=10)
            corners = corners.reshape(-1, 2) + np.array([x_min, y_min])
            corners[:, 0] = np.clip(corners[:, 0], x_min, x_max)
            corners[:, 1] = np.clip(corners[:, 1], y_min, y_max)
            return np.array([[corner] for corner in corners]).astype(np.float32)

    def main(self):
        while True:
            _, frame = self.cap.read()
            next_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            zone_selected = self.rect_start is not None and self.rect_end is not None
            if zone_selected:
                for i, point in enumerate(self.tracking_points):
                    if not np.array_equal(point, [[np.inf, np.inf]]):
                        new_point, status, error = cv2.calcOpticalFlowPyrLK(prevImg=self.prev_img,
                                                                            nextImg=next_img,
                                                                            prevPts=np.array([point]),
                                                                            nextPts=None,
                                                                            **self.lk_params)
                        good_new = new_point[status.flatten() == 1]
                        good_old = point[status.flatten() == 1]
                        for new, old in zip(good_new, good_old):
                            a, b = new.ravel()
                            c, d = old.ravel()
                            frame = cv2.line(frame, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 2)
                            frame = cv2.circle(frame, (int(a), int(b)), 5, (0, 255, 0), -1)
                        if good_new.size == 2:
                            self.tracking_points[i] = good_new
                        else:
                            print(f'Pixel n°{i} was lost.')
                            self.tracking_points[i] = [[np.inf, np.inf]]
            self.prev_img = next_img.copy()
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF in [ord('q')]:
                break
        cv2.destroyAllWindows()


if __name__ == '__main__':
    tracker = PoiTracker(camera=0, num_points=20)
    print(tracker.camera)
    print('hi')
    tracker.main()
