from icecream import ic
import numpy as np
import cv2


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
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

RECT_START = (-1, -1)
RECT_END = (-1, -1)
selecting_rect = False

tracked_points = []

while True:
    _, frame = cap.read()

    if RECT_START[0] != -1 and RECT_END[0] != -1:
        cv2.rectangle(frame, RECT_START, RECT_END, (0, 255, 0), 2)

        if not selecting_rect:
            tracked_points = generate_mesh(RECT_START, RECT_END)

        if tracked_points:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if 'old_frame' not in globals():
                print('Old frame was not right')
                old_frame = gray_frame.copy()
            print('Now fixed')
            ic(np.array(tracked_points).shape, np.array(tracked_points).T)
            new_points, status, _ = cv2.calcOpticalFlowPyrLK(old_frame, gray_frame, np.array(tracked_points), None, **lk_params)

            good_new = new_points[status == 1]
            good_old = np.array(tracked_points)[status.flatten() == 1]

            for new, old in zip(good_new, good_old):
                a, b = new.ravel()
                c, d = old.ravel()
                frame = cv2.line(frame, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 2)
                frame = cv2.circle(frame, (int(a), int(b)), 5, (0, 255, 0), -1)

            tracked_points = good_new.tolist()

    # old_frame = gray_frame.copy()
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        break

cap.release()
cv2.destroyAllWindows()
