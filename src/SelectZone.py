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
    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1) & 0xFF
    if key in [ord('q')]:
        break

cv2.destroyAllWindows()
