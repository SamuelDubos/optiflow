import cv2
import numpy as np


def select_point(event, x, y, flags, param):
    global point, point_selected, old_points
    if event == cv2.EVENT_LBUTTONDOWN:
        point = (x, y)
        point_selected = True
        old_points = np.array([[x, y]], dtype=np.float32)


cap = cv2.VideoCapture(0)
cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame', select_point)
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

point_selected = False
point = ()
old_points = None
old_frame = None

while True:
    _, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if point_selected:
        new_points, status, error = cv2.calcOpticalFlowPyrLK(old_frame, gray_frame, old_points, None, **lk_params)
        good_new = new_points[status.flatten() == 1]
        good_old = old_points[status.flatten() == 1]
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            frame = cv2.line(frame, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 2)
            frame = cv2.circle(frame, (int(a), int(b)), 5, (0, 255, 0), -1)
        old_points = good_new
    old_frame = gray_frame.copy()
    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1) & 0xFF
    if key in [ord('q')]:
        break

cv2.destroyAllWindows()
