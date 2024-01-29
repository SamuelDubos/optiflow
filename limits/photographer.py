"""
TODO: Docstring

Author: @SamuelDubos
Date: January 29, 2024
"""

import numpy as np
import shutil
import cv2
import os


class Photographer:
    def __init__(self, camera, folder, run=False):
        self.camera = camera
        self.folder = os.path.join('limits', 'images', folder)
        self.click_coordinates = []
        self.frame = None
        self.ndarray = os.path.join('limits', 'images', f'{folder}_coordinates.npy')
        self.run() if run else None

    def mouse_click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(f'Click Position : ({x}, {y})')
            self.click_coordinates.append((x, y))
            index = len(os.listdir(self.folder))
            image_name = os.path.join(self.folder, f'webcam_{index}.jpg')
            cv2.imwrite(image_name, self.frame)
            print(f'Image saved : {image_name}')

    def capture_webcam(self):
        cap = cv2.VideoCapture(self.camera, cv2.CAP_DSHOW)
        if not cap.isOpened():
            print('Error: Unable to open webcam.')
            exit()
        cv2.namedWindow('Webcam')
        cv2.setMouseCallback('Webcam', self.mouse_click)
        while True:
            ret, self.frame = cap.read()
            cv2.imshow('Webcam', self.frame)
            if cv2.waitKey(1) & 0xFF in [ord('q')]:
                break
        cv2.destroyAllWindows()
        cap.release()

    def save_coordinates(self):
        if os.path.exists(self.ndarray):
            coordinates_array = np.concatenate((np.load(self.ndarray), np.array(self.click_coordinates)))
        else:
            coordinates_array = np.array(self.click_coordinates)
        np.save(self.ndarray, coordinates_array)
        print(f'Click coordinates have been saved to {self.ndarray}.')

    @staticmethod
    def onerror(func, path):
        import stat
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def delete(self):
        print(f'Deleting {self.folder} folder')
        try:
            n_images = len(os.listdir(self.folder))
            shutil.rmtree(self.folder, onerror=self.onerror)
            print(f'All {n_images} images have been deleted.')
        except OSError as e:
            print(f'Error: {e.filename} - {e.strerror}.')
        if os.path.exists(self.ndarray):
            os.remove(self.ndarray)
            print('Numpy ndarray file has been deleted.')

    def run(self):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        self.capture_webcam()
        self.save_coordinates()


if __name__ == '__main__':
    photographer = Photographer(camera=0, folder='CAG107')
    photographer.run()
