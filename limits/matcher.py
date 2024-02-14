"""
PhotographsMatcher: A utility to match pixels in real-time
with pixels saved from previous photographs.

Author: @SamuelDubos
Date: February 14, 2024
"""

import numpy as np
import cv2
import os


class PhotographsMatcher:

    def __init__(self, camera, photographer):
        """
        Initialize the PhotographsMatcher object.

        Parameters:
        - camera: Index of the camera to use for video capture.
        - photographer: Instance of the Photographer class to access captured photographs and coordinates.
        """
        self.camera = camera
        self.photographer = photographer
        self.points = np.load(self.photographer.ndarray)

        self.point = None
        self.frames = []
        self.found = 0

        # Initialize video capture
        self.cap = cv2.VideoCapture(self.camera, cv2.CAP_DSHOW)
        cv2.namedWindow('Frame')

        # Parameters for Lucas-Kanade optical flow
        self.lk_params = dict(winSize=(15, 15),
                              maxLevel=2,
                              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    def main(self):
        """
        Main function to match pixels in real-time with pixels saved from previous photographs.
        """
        while True:
            self.found = 0
            _, frame = self.cap.read()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            for i, image in enumerate(os.listdir(self.photographer.folder)):
                image = cv2.resize(cv2.imread(f'{self.photographer.folder}/{image}'), (640, 480))
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                point = np.array([self.points[i]]).astype(np.float32)
                frame = cv2.circle(frame, (int(point[0, 0]), int(point[0, 1])), 5, (255, 0, 0), -1)
                new_point, status, error = cv2.calcOpticalFlowPyrLK(gray_image,
                                                                    gray_frame,
                                                                    point,
                                                                    None,
                                                                    **self.lk_params)
                good_new = new_point[status.flatten() == 1]
                good_old = point[status.flatten() == 1]
                self.found += int(good_old.size / 2)
                for new, old in zip(good_new, good_old):
                    a, b = new.ravel()
                    c, d = old.ravel()
                    frame = cv2.line(frame, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 2)
                    frame = cv2.circle(frame, (int(a), int(b)), 5, (0, 255, 0), -1)
                    frame = cv2.circle(frame, (int(c), int(d)), 5, (0, 0, 255), -1)
            cv2.imshow('Frame', frame)
            percentage = self.found / len(self.points)
            print(f'\rFound pixels: {self.found} out of {len(self.points)} ({percentage:.1%})', end='')
            key = cv2.waitKey(1) & 0xFF
            if key in [ord('q')]:
                break
        cv2.destroyAllWindows()
