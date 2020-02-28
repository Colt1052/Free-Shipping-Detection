
import sys
import cv2
from PyQt5.QtWidgets import QApplication
from Scripts.VideoGrabber import Camera
from Scripts.VideoGrabber import Video
from Scripts.Windows import StartWindow
from Scripts.ObjectTracker import Tracker
from Scripts.ObjectTracker import Detector
from Scripts.ObjectTracker import Finder



# count the arguments
arguments = len(sys.argv) - 1

# output argument-wise
position = 1
while (arguments >= position):
    print ("parameter %i: %s" % (position, sys.argv[position]))
    position = position + 1



grabber = Camera(0)
#grabber = Video("C:/Users/colto/Desktop/Free-Shipping-Detection/Videos/MP4/First Drone Flight Showing Jello Effect Of Vibrations On Camera.mp4")
grabber.initialize()

finder = Finder(grabber)


while True:
    finder.Finding()

    #grabber.getFrame()
    #print(str(grabber.FPS))

    k = cv2.waitKey(1) & 0xff
    if k == 27: break

#app = QApplication([])
#start_window = StartWindow(grabber)
#start_window.show()
#app.exit(app.exec_())