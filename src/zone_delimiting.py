"""
Zone delimiter utility for defining regions of interest on screen.

Author: @SamuelDubos
Date: February 14, 2024
"""

import numpy as np
import cv2


class ZoneDelimiter:

    def __init__(self, camera, mesh=False):
        """
        Initialize the ZoneDelimiter object.

        Parameters:
        - camera: Index of the camera to use for video capture.
        - mesh: Boolean indicating whether to generate a mesh over the selected region.
        """
        self.camera = camera
        self.mesh = mesh

        # Initialize variables for rectangle selection
        self.rect_start = None
        self.rect_end = None
        self.selecting_rect = False

        # Initialize video capture
        self.cap = cv2.VideoCapture(self.camera)

        # Create a window and set mouse callback function
        cv2.namedWindow('Frame')
        cv2.setMouseCallback('Frame', self.select_rect)

    def select_rect(self, event, x, y, flags, param):
        """
        Mouse callback function to select a rectangle on the screen.

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

    def generate_mesh(self, grid_size=10):
        """
        Generate a mesh of points within the selected rectangle.

        Parameters:
        - grid_size: Number of points along each axis.

        Returns:
        - List of points within the rectangle.
        """
        points = []
        x_range = np.linspace(self.rect_start[0], self.rect_end[0], grid_size)
        y_range = np.linspace(self.rect_start[1], self.rect_end[1], grid_size)
        for y in y_range:
            for x in x_range:
                points.append((int(x), int(y)))
        return points

    def main(self):
        """
        Main function to define zones of interest and display them on the screen.
        """
        while True:
            _, frame = self.cap.read()
            if self.rect_start is not None and self.rect_end is not None:
                # Draw the rectangle on the frame
                cv2.rectangle(frame, self.rect_start, self.rect_end, (0, 255, 0), 2)
                if self.mesh:
                    # Generate and display the mesh points
                    tracked_points = self.generate_mesh()
                    for point in tracked_points:
                        cv2.circle(frame, point, 3, (0, 0, 255), -1)
            cv2.imshow('Frame', frame)
            key = cv2.waitKey(1) & 0xFF
            if key in [ord('q')]:
                break

        # Release the video capture and close all windows
        cv2.destroyAllWindows()


if __name__ == '__main__':
    # Create a ZoneDelimiter object with camera index 0
    tracker = ZoneDelimiter(camera=0)
    # Start defining zones of interest
    tracker.main()
