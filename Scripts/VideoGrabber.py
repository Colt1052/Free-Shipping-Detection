import numpy as np

import cv2

class Camera:
    def __init__(self, cam_num):
        self.cam_num = cam_num
        self.cap = None
        self.last_frame = np.zeros((1,1))

    def initialize(self):
        self.cap = cv2.VideoCapture(self.cam_num)

    def get_frame(self):
        ret, self.last_frame = self.cap.read()
        return self.last_frame

    def acquire_movie(self, num_frames):
        movie = []
        for _ in range(num_frames):
            movie.append(self.get_frame())
        return movie

    def close_camera(self):
        self.cap.release()

    def __str__(self):
        return 'OpenCV Camera {}'.format(self.cam_num)

class Video:
    def __init__(self, file_name):
        self.file_name = file_name
        self.last_frame = np.zeros((1,1))

    def initialize(self):
        self.video = cv2.VideoCapture(self.file_name)
        if not self.video.isOpened():
            print("Could not open video")

    def get_frame(self,scale = 1):
        ok, frame = self.video.read()
        scaled = cv2.resize(frame,(int(np.shape(frame)[1]*scale),int(np.shape(frame)[0]*scale)))
        return scaled


    def getROI(self):
        ok, frame = self.video.read()
        if not ok:
            print('Cannot read video file')
        bbox = cv2.selectROI(frame, False)
        return bbox


    def close_video(self):
        self.video = None

    def __str__(self):
        return 'Video: {}'.format(self.file_name)

if __name__ == '__main__':
    cam = Camera(0)
    cam.initialize()
    print(cam)

    frame = cam.get_frame()
    print(frame)
    cam.close_camera()