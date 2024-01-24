import numpy as np
import cv2
import sys


class ZoneTracker:

    def __init__(self, camera):
        self.camera = camera

        self.rect_start = None
        self.rect_end = None
        self.selecting_rect = False

        self.cap = cv2.VideoCapture(self.camera)
        cv2.namedWindow('Frame')
        cv2.setMouseCallback('Frame', self.select_rect)

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

    def generate_mesh(self, grid_size=10):
        points = []
        x_range = np.linspace(self.rect_start[0], self.rect_end[0], grid_size)
        y_range = np.linspace(self.rect_start[1], self.rect_end[1], grid_size)
        for y in y_range:
            for x in x_range:
                points.append((int(x), int(y)))
        return points

    def main(self, mesh=False):
        while True:
            _, frame = self.cap.read()
            if self.rect_start is not None and self.rect_end is not None:  # TODO: Handle second rectangle
                cv2.rectangle(frame, self.rect_start, self.rect_end, (0, 255, 0), 2)
                if mesh:
                    tracked_points = self.generate_mesh()
                    for point in tracked_points:
                        cv2.circle(frame, point, 3, (0, 0, 255), -1)
            cv2.imshow('Frame', frame)
            key = cv2.waitKey(1) & 0xFF
            if key in [ord('q')]:
                break
        cv2.destroyAllWindows()


if __name__ == '__main__':
    tracker = ZoneTracker(camera=0)
    tracker.main(bool(sys.argv[1]) if len(sys.argv) >= 2 else False)
