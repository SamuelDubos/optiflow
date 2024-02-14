"""
Point of Interest (POI) Identifier: A utility to identify points of interest within a selected region.

Author: @SamuelDubos
Date: February 14, 2024
"""

import numpy as np
import cv2


class PoiIdentifier:

    def __init__(self, camera, num_points):
        """
        Initialize the POI Identifier object.

        Parameters:
        - camera: Index of the camera to use for video capture.
        - num_points: Number of points of interest to identify.
        """
        self.camera = camera
        self.num_points = num_points
        self.rect_start = None
        self.rect_end = None
        self.selecting_rect = False
        self.tracking_points = []

        # Initialize video capture
        self.cap = cv2.VideoCapture(self.camera)

        # Create a window and set mouse callback function
        cv2.namedWindow('Frame')
        cv2.setMouseCallback('Frame', self.select_rect)

    def select_rect(self, event, x, y, flags, param):
        """
        Mouse callback function to select a rectangle on the screen and identify points of interest within it.

        Parameters:
        - event: Type of mouse event.
        - x, y: Coordinates of the mouse cursor.
        - flags: Additional flags.
        - param: Additional parameters.
        """
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
        """
        Generate points of interest within the selected rectangle.

        Parameters:
        - frame: Image frame from which points of interest are generated.

        Returns:
        - List of points of interest.
        """
        if self.rect_start is not None and self.rect_end is not None:
            x_min, y_min = np.min([self.rect_start, self.rect_end], axis=0).ravel()
            x_max, y_max = np.max([self.rect_start, self.rect_end], axis=0).ravel()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners = cv2.goodFeaturesToTrack(gray_frame[y_min:y_max, x_min:x_max],
                                              maxCorners=self.num_points, qualityLevel=0.01, minDistance=10)
            corners = corners.reshape(-1, 2) + np.array([x_min, y_min])
            corners[:, 0] = np.clip(corners[:, 0], x_min, x_max)
            corners[:, 1] = np.clip(corners[:, 1], y_min, y_max)
            return corners.astype(int)

    def main(self):
        """
        Main function to select a region and identify points of interest within it.
        """
        while True:
            _, frame = self.cap.read()
            if self.rect_start is not None and self.rect_end is not None:
                cv2.rectangle(frame, self.rect_start, self.rect_end, (0, 255, 0), 2)
                for point in self.tracking_points:
                    x, y = point
                    cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)
            cv2.imshow('Frame', frame)
            key = cv2.waitKey(1) & 0xFF
            if key in [ord('q')]:
                break
        cv2.destroyAllWindows()


if __name__ == '__main__':
    # Create a PoiIdentifier object with camera index 0 and 10 points of interest
    tracker = PoiIdentifier(camera=0, num_points=10)
    # Start the main functionality to identify points of interest
    tracker.main()
