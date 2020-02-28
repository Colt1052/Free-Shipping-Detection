import numpy as np
import time
import sys

import cv2

class Camera:
    def __init__(self, cam_num):
        self.cam_num = cam_num
        self.video = None
        self.last_frame = np.zeros((1,1))
        self.last_frame_time = time.time()
        self.FPS = 0

    def initialize(self):
        self.video = cv2.VideoCapture(self.cam_num)

        # Read first frame.
        ok, frame = self.video.read()
        if not ok:
            print('Cannot read video file')
            sys.exit()

    def getFrame(self,scale = 1):
        ret, self.last_frame = self.video.read()
        scaled = cv2.resize(self.last_frame, (int(np.shape(self.last_frame)[1] * scale), int(np.shape(self.last_frame)[0] * scale)))
        self.FPS = 1/(time.time()-self.last_frame_time)
        self.last_frame_time = time.time()
        return ret,scaled

    def getLastFrame(self, scale=1):
        scaled = self.last_frame
        if not scale == 1:
            scaled = cv2.resize(self.last_frame,
                                (int(np.shape(self.last_frame)[1] * scale), int(np.shape(self.last_frame)[0] * scale)))
        return scaled
    def acquire_movie(self, num_frames):
        movie = []
        for _ in range(num_frames):
            movie.append(self.getFrame())
        return movie

    def close_camera(self):
        self.video.release()

    def isOpened(self):
        return self.video.isOpened()

    def __str__(self):
        return 'OpenCV Camera {}'.format(self.cam_num)

class Video:
    def __init__(self, file_name):
        self.file_name = file_name
        self.last_frame = np.zeros((1,1))
        self.last_frame_time = time.time()

    def initialize(self):
        self.video = cv2.VideoCapture(self.file_name)
        if not self.video.isOpened():
            print("Could not open video")

    def getFrame(self,scale = 1):
        ok, frame = self.video.read()
        self.last_frame = frame
        scaled = frame
        if ok:
            if not scale == 1:
                scaled = cv2.resize(frame,(int(np.shape(frame)[1]*scale),int(np.shape(frame)[0]*scale)))
            if time.time()-self.last_frame_time < (1.0/60.0):
                time.sleep((1.0/60.0)-(time.time()-self.last_frame_time))
            self.FPS = 1.0 / (time.time() - self.last_frame_time)
            self.last_frame_time = time.time()
        return ok,scaled
    def getLastFrame(self,scale = 1):
        scaled = self.last_frame
        if not scale == 1:
            scaled = cv2.resize(self.last_frame, (int(np.shape(self.last_frame)[1] * scale), int(np.shape(self.last_frame)[0] * scale)))
        return scaled
    def isOpened(self):
        return self.video.isOpened()

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

    frame = cam.getFrame()
    print(frame)
    cam.close_camera()