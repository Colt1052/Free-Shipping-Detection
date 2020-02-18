import numpy as np

from PyQt5.QtCore import Qt, QThread, QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QApplication,QLabel,QLineEdit,QHBoxLayout
from PyQt5.QtGui import QPixmap,QImage
from pyqtgraph import ImageView
import time


class StartWindow(QMainWindow):
    def __init__(self, grabber=None):
        super().__init__()
        self.grabber = grabber

        #self.central_widget = QWidget()
        self.h_central = QWidget()
        self.button_stop = QPushButton('Stop Video')
        self.button_start = QPushButton('Start Movie')
        self.image_view = QLabel()
        self.testing = QPushButton("Testing123")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button_stop)
        self.layout.addStretch()
        self.layout.addWidget(self.button_start)
        self.layout.addWidget(self.image_view)


        self.h_layout = QHBoxLayout(self.h_central)
        self.h_layout.addLayout(self.layout)
        self.h_layout.addWidget(self.testing)
        self.setCentralWidget(self.h_central)

        self.button_stop.clicked.connect(self.stop_feed)
        self.button_start.clicked.connect(self.start_video)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_movie)

    def update_image(self):
        print("in function")
        frame = self.grabber.get_frame()
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        Img = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.image_view.setPixmap(QPixmap.fromImage(Img))

    def stop_feed(self):
        self.video_thread.paused = True

        #self.image_view.setImage(frame.T)
    def update_movie(self):
        frame = self.grabber.get_frame()
        #self.image_view.setImage(self.camera.last_frame.T)
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        Img = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.image_view.setPixmap(QPixmap.fromImage(Img))

    def start_video(self):
        self.video_thread = VideoThread(self.grabber,self.image_view)
        self.video_thread.start()
        #self.update_timer.start(30)


class VideoThread(QThread):
    def __init__(self, grabber,image_view):
        super().__init__()

        self.grabber = grabber
        self.paused = False
        self.image_view = image_view

    def run(self):
        while not self.paused:
            self.update_image()


    def update_image(self):
        frame = self.grabber.get_frame(0.2)
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        Img = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.image_view.setPixmap(QPixmap.fromImage(Img))




if __name__ == '__main__':
    app = QApplication([])
    window = StartWindow()
    window.show()
    app.exit(app.exec_())