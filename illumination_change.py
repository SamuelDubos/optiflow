import numpy as np
import cv2
import time


class Pixel_Light_Test:
    """
    This class is used to run tests on the effect of light variance on LK methods. 

    The results: even small changes in light (overall brightness), if they happen quickly, will shift the points around. 
    If the changes are gradual, the pixels are much more likely to stay (or barely move).
    """

    def __init__(self):
        """
        Initialize the Pixel_Light_Test object.

        Parameters: none
        """
        self.camera = 0
        self.point_selected = False
        self.point = None
        self.old_point = None
        self.old_frame = None

        #self.cap = cv2.VideoCapture(self.camera, cv2.CAP_DSHOW)
        self.cap = cv2.VideoCapture(self.camera)
        if not self.cap.isOpened():
            print("Camera not opened")
        cv2.namedWindow('Frame')
        cv2.setMouseCallback('Frame', self.select_point)
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
            self.point = (x, y)  # TODO: Now useless?
            self.point_selected = True
            self.old_point = np.array([[x, y]], dtype=np.float32)

    def main(self, coeff:float, gradual:bool, max_rounds:int=0, wait:int=3):
        """
        This is the main function to launch the brightness study. First choose a coefficient (coeff), then if the change 
        is to be gradual or not, and eventually the other parameters if it will be gradual.

        Be sure to select a point early to observe its changes in position.

        Parameters:
        - coeff: The degree to which the brightness will change. The range for coeff is [-1; 1], it is used 
        to modify the "value" (from HSV) in the image. This is done to test the resilience of LK to illumination 
        changes. coeff in [-1; 0[ are used to darken the image, with -1 setting the global image "value" at 0 
        coeff in [0; 1] are used to brighten the image, with 1 setting the global image "value" at 255.
        - gradual: Determines if the change in brightness is gradual or not. If not, then it happens after 5 seconds. 
        If it is, then after max_rounds * wait seconds the simulation will have reached coeff and end.
        - max_rounds: If change is gradual, then it occurs over this many rounds.
        - wait: If change is gradual, then this sets the number of seconds to wait between each round.
        """
        start_time = time.time()
        if (coeff<-1 or coeff>1):
            raise Exception("coeff not within [-1; 1]")
        while True:
            _, frame = self.cap.read()
            if not gradual:
                if coeff<0:
                    if time.time()-start_time>5.0:
                        frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                        frame1[:,:,2] = (frame1[:,:,2]*(1+coeff)).astype(np.uint8)
                        frame = cv2.cvtColor(frame1, cv2.COLOR_HSV2BGR)
                elif coeff>=0:
                    if time.time()-start_time>5.0:
                        frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                        delta = coeff*(np.uint8(255-np.min(frame1[:,:,2])))
                        frame1[:,:,2] = (np.where(frame1[:,:,2]<(255-delta), frame1[:,:,2]+delta, 255*np.full_like(frame1[:,:,2], 1))).astype(np.uint8)
                        frame = cv2.cvtColor(frame1, cv2.COLOR_HSV2BGR)
            if gradual:
                round_counter = round(time.time()-start_time)//wait
                if (coeff<0 and round_counter<=max_rounds):
                    partial_coeff = coeff*(round_counter/max_rounds)
                    frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    frame1[:,:,2] = (frame1[:,:,2]*(1+partial_coeff)).astype(np.uint8)
                    frame = cv2.cvtColor(frame1, cv2.COLOR_HSV2BGR)
                elif (coeff>=0 and round_counter<=max_rounds):
                    partial_coeff = coeff*(round_counter/max_rounds)
                    frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    delta = partial_coeff*(np.uint8(255-np.min(frame1[:,:,2])))
                    frame1[:,:,2] = (np.where(frame1[:,:,2]<(255-delta), frame1[:,:,2]+delta, 255*np.full_like(frame1[:,:,2], 1))).astype(np.uint8)
                    frame = cv2.cvtColor(frame1, cv2.COLOR_HSV2BGR)
                if round_counter>max_rounds:
                    break
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if self.point_selected:
                new_point, status, error = cv2.calcOpticalFlowPyrLK(self.old_frame,
                                                                    gray_frame,
                                                                    self.old_point,
                                                                    None,
                                                                    **self.lk_params)
                good_new = new_point[status.flatten() == 1]
                good_old = self.old_point[status.flatten() == 1]
                for new, old in zip(good_new, good_old):
                    a, b = new.ravel()
                    c, d = old.ravel()
                    frame = cv2.line(frame, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 2)
                    frame = cv2.circle(frame, (int(a), int(b)), 5, (0, 255, 0), -1)
                self.old_point = good_new
            self.old_frame = gray_frame.copy()
            cv2.imshow('Frame', frame)
            key = cv2.waitKey(1) & 0xFF
            if key in [ord('q')]:
                break
        cv2.destroyAllWindows()

Pixel_Light_Test().main(-0.4, True, 20, 3)