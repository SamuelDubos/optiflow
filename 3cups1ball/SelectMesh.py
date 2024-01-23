import cv2
import numpy as np


def select_rect(event, x, y, flags, param):
    global RECT_START, RECT_END, selecting_rect
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'Click down on {x, y}')
        RECT_START = (x, y)
        selecting_rect = True
    elif event == cv2.EVENT_LBUTTONUP:
        print(f'Click up on {x, y}')
        RECT_END = (x, y)
        selecting_rect = False


def generate_mesh(rect_start, rect_end, grid_size=10):
    points = []
    x_range = np.linspace(rect_start[0], rect_end[0], grid_size)
    y_range = np.linspace(rect_start[1], rect_end[1], grid_size)
    for y in y_range:
        for x in x_range:
            points.append((int(x), int(y)))
    return points


cap = cv2.VideoCapture(0)
cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame', select_rect)

RECT_START = (-1, -1)
RECT_END = (-1, -1)
selecting_rect = False

while True:
    _, frame = cap.read()
    if RECT_START[0] != -1 and RECT_END[0] != -1:
        cv2.rectangle(frame, RECT_START, RECT_END, (0, 255, 0), 2)
        tracked_points = generate_mesh(RECT_START, RECT_END)
        for point in tracked_points:
            cv2.circle(frame, point, 3, (0, 0, 255), -1)
    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1) & 0xFF
    if key in [ord('q')]:
        break

cv2.destroyAllWindows()
