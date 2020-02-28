import cv2
import sys
import os
import scipy
from matplotlib import pyplot as plt
import numpy as np
import time

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

class Tracker:
    def __init__(self,tracker_type,grabber,bbox):
        tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
        self.video_grabber = grabber
        self.initVideo()
        self.bbox = bbox
        if int(minor_ver) < 3 and int(major_ver) <= 3:
            self.tracker = cv2.Tracker_create(tracker_type)
        else:
            if tracker_type == 'BOOSTING':
                self.tracker = cv2.TrackerBoosting_create()
            if tracker_type == 'MIL':
                self.tracker = cv2.TrackerMIL_create()
            if tracker_type == 'KCF':
                self.tracker = cv2.TrackerKCF_create()
            if tracker_type == 'TLD':
                self.tracker = cv2.TrackerTLD_create()
            if tracker_type == 'MEDIANFLOW':
                self.tracker = cv2.TrackerMedianFlow_create()
            if tracker_type == 'GOTURN':
                self.tracker = cv2.TrackerGOTURN_create()
            if tracker_type == 'MOSSE':
                self.tracker = cv2.TrackerMOSSE_create()
            if tracker_type == "CSRT":
                self.tracker = cv2.TrackerCSRT_create()

        # Initialize tracker with first frame and bounding box
        ok = self.tracker.init(self.video_grabber.last_frame, bbox)

    def initVideo(self,videoName):

        if(self.video_grabber.isOpened()):
            print("video initialized successfully")
        else:
            print("video initialization FAILED")
            sys.exit()

    def Tracking(self):
        # Read a new frame
        ok, frame = self.video_grabber.getFrame()
        if not ok:
            return

        # Update tracker
        ok, self.bbox = self.tracker.update(frame)

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(self.bbox[0]), int(self.bbox[1]))
            p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 10, 1)
        else:
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        # Display result
        self.display_frame = frame

    def Display(self):
        cv2.imshow("Tracking", self.display_frame)


class Detector:
    def __init__(self,name):
        print("testing")

class Finder:
    def __init__(self,grabber):
        self.trackable_objects = []
        self.video_grabber = grabber
        self.initVideo()
        self.thresh = 0
        self.lastFrame = np.zeros(1)



    def initVideo(self):
        if(self.video_grabber.isOpened()):
            print("video initialized successfully")
        else:
            print("video initialization FAILED")
            sys.exit()

    def Finding(self):

        k = cv2.waitKey(1)
        #print(k)
        if k == 122 or not self.thresh == 0 and self.thresh < 255 and not k == 120:
            print(self.thresh)
            gray = cv2.cvtColor(self.video_grabber.getLastFrame(0.4), cv2.COLOR_BGR2GRAY)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            laplacian[laplacian < self.thresh] = 0
            laplacian[laplacian >= self.thresh] = 255
            time.sleep(0.8)
            self.display_frame = laplacian
            self.Disply()
            self.thresh = self.thresh+1
        else:
            self.thresh = 0
            ok, frame = self.video_grabber.getFrame()
            if not ok:
                return

            # Display result
            cv2.putText(frame, "FPS : " + str(int(self.video_grabber.FPS)), (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 4,
                        (50, 170, 50), 2);

            gray = cv2.cvtColor(self.video_grabber.getLastFrame(0.4), cv2.COLOR_BGR2GRAY)
            Difference = cv2.subtract(self.lastFrame,gray)
            #Difference[Difference > 255] = 255
            Difference = np.uint8(Difference)

            cv2.imshow("Gray", gray)
            cv2.imshow("LastGray",self.lastFrame)

            self.lastFrame = gray
            ret, thresh1 = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
            gray_blur = cv2.blur(gray, (3, 3))

            laplacian = cv2.Laplacian(gray_blur, cv2.CV_64F)
            # the cv2 version of the fourier transform is much faster than numpy
            fourier = np.fft.fft2(gray)
            fshift = np.fft.fftshift(fourier)
            magnitude_spectrum = 20*np.log(np.abs(fshift))
            magnitude_spectrum = np.asarray(magnitude_spectrum,dtype = np.uint8)
            laplacian_og = laplacian
            cv2.imshow("laplacian_og", laplacian_og)
            laplacian[laplacian < 10] = 0
            laplacian[laplacian >= 10] = 255

            #laplacian[laplacian == 255] = 10
            #laplacian[laplacian == 0] = 255
            #laplacian[laplacian == 10] = 0
            laplacian = laplacian.astype(np.uint8)
            #opening = cv2.morphologyEx(laplacian, cv2.MORPH_OPEN, (10,10),iterations=8)
            closing = cv2.morphologyEx(laplacian, cv2.MORPH_CLOSE, (10,10),iterations=15)
            #kernel = np.ones((2, 2), np.float32) / 225
            #smoothed = cv2.filter2D(laplacian, -1, kernel)
            #smoothed2 = cv2.filter2D(smoothed, -1, kernel)
            #dilation = cv2.dilate(laplacian, kernel, iterations=1)
            laplacian = laplacian.astype(np.uint8)
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
            #dilation = dilation.astype(np.uint8)
            blur = cv2.blur(laplacian, (2, 2))
            cv2.imshow("blur", blur)
            blur2 = blur
            blur2[blur2 < 255] = 0
            blur2[blur2 >= 255] = 255
            cv2.imshow("blur2", blur2)
            edged = cv2.Canny(laplacian, 254,255)
            dilation = cv2.dilate(edged, (3,3), iterations=2)
            #edged = cv2.Canny(edged, 254, 255)
            contours, hierarchy = cv2.findContours(dilation,
            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            areas_dic = {}
            epsilons_dic = {}
            areas = []
            epsilons = []
            area_perimeter_ratio = []
            area_perimeter_ratio_dic = {}
            for (i, c) in enumerate(contours):
                area = cv2.contourArea(c)
                epsilon = 0.1 * cv2.arcLength(c, True)
                #epsilon = cv2.convexHull(c)
                epsilons_dic[area] = epsilon
                areas_dic[area] = c
                epsilons.append(epsilon)
                areas.append(area)
                if not epsilon == 0:
                    area_perimeter_ratio_dic[area] = area/epsilon
                    area_perimeter_ratio.append(area/epsilon)


            epsilons.sort(reverse = True)
            areas.sort(reverse = True)
            area_perimeter_ratio.sort(reverse = True)
            contours_found = False
            i = 0
            max_contours = []
            while not contours_found:
                if areas.__len__() > 0:
                    area = areas[i]
                    #a_p_r = area_perimeter_ratio_dic[area]
                    #print(a_p_r)
                    #if(a_p_r < 4 and i < 15):
                    #    max_contours.append(areas_dic[areas[i]])


                if(max_contours.__len__() >= 3 or i > areas.__len__()-2):
                    contours_found = True
                i = i+1

            #max_contours = [areas_dic[areas[0]],areas_dic[areas[1]],areas_dic[areas[2]]]
            #cv2.drawContours(gray, max_contours, -1, (0, 255, 0), 3)
            #cv2.fillPoly(gray, contours, (255, 0, 0))

            cv2.imshow("closing", closing)
            #cv2.imshow("opening", opening)
            #cv2.imshow("diltion", dilation)
            cv2.imshow("edged", edged)
            cv2.imshow("contours", gray)
            cv2.imshow("laplacian", laplacian)
            cv2.imshow("dilation", dilation)
            cv2.imshow("sobelx", sobelx)
            cv2.imshow("sobely", sobely)
            cv2.imshow("Difference", Difference)
            cv2.imshow("fourier", magnitude_spectrum)

            self.display_frame = laplacian
            self.Disply()
            #self.Print()



    def Print(self):
        print("FPS: " + str(self.video_grabber.FPS))
    def Disply(self):
        cv2.imshow("Finder", self.display_frame)
