"""
Track a manually defined pixel on the screen using Lucas-Kanade.

Author: @SamuelDubos
Date: February 14, 2024
"""

import numpy as np
import cv2


class PixelTracker:

    def __init__(self, camera):
        """
        Initialize the PixelTracker object.

        Parameters:
        - camera: Index of the camera to use for video capture.
        """
        self.camera = camera

        # Initialize variables for point selection and tracking
        self.point_selected = False
        self.old_point = None
        self.old_frame = None

        # Initialize video capture
        self.cap = cv2.VideoCapture(self.camera, cv2.CAP_DSHOW)

        # Create a window and set mouse callback function
        cv2.namedWindow('Frame')
        cv2.setMouseCallback('Frame', self.select_point)

        # Parameters for Lucas-Kanade optical flow
        self.lk_params = dict(winSize=(15, 15),
                              maxLevel=2,
                              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    def select_point(self, event, x, y, flags, param):
        """
        Mouse callback function to select a point on the screen.

        Parameters:
        - event: Type of mouse event.
        - x, y: Coordinates of the mouse cursor.
        - flags: Additional flags.
        - param: Additional parameters.
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            # Set the selected point
            self.point_selected = True
            self.old_point = np.array([[x, y]], dtype=np.float32)

    def main(self):
        """
        Main function to track the selected pixel using Lucas-Kanade method.
        """
        while True:
            # Capture frame-by-frame
            _, frame = self.cap.read()
            new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Track the selected point using Lucas-Kanade optical flow
            if self.point_selected:
                new_point, status, error = cv2.calcOpticalFlowPyrLK(self.old_frame,
                                                                    new_frame,
                                                                    self.old_point,
                                                                    None,
                                                                    **self.lk_params)
                # Select good points
                good_new = new_point[status.flatten() == 1]
                good_old = self.old_point[status.flatten() == 1]

                # Draw tracks
                for new, old in zip(good_new, good_old):
                    a, b = new.ravel()
                    c, d = old.ravel()
                    frame = cv2.line(frame, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 2)
                    frame = cv2.circle(frame, (int(a), int(b)), 5, (0, 255, 0), -1)

                self.old_point = good_new

            self.old_frame = new_frame.copy()

            # Display the frame
            cv2.imshow('Frame', frame)

            # Check for user input to quit the program
            key = cv2.waitKey(1) & 0xFF
            if key in [ord('q')]:
                break

        # Release the video capture and close all windows
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    # Create a PixelTracker object with camera index 0
    tracker = PixelTracker(0)
    # Start tracking the pixel
    tracker.main()
