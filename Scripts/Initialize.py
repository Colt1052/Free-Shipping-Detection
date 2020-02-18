
from PyQt5.QtWidgets import QApplication

from Scripts.VideoGrabber import Camera
from Scripts.VideoGrabber import Video
from Scripts.Windows import StartWindow

#grabber = Camera(0)
grabber = Video("C:/Users/colto/Desktop/Free-Shipping-Detection/Videos/MP4/Rotation_and_Detection.mp4")
grabber.initialize()

app = QApplication([])
start_window = StartWindow(grabber)
start_window.show()
app.exit(app.exec_())