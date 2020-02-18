import cv2
import sys
import os
import numpy as np

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

if __name__ == '__main__':

    # Set up tracker.
    # Instead of MIL, you can also use

    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[6]

    if int(minor_ver) < 3 and int(major_ver) <= 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        if tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()

    # Read video
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    print(ROOT_DIR)
    video = cv2.VideoCapture(ROOT_DIR.replace("\Scripts",'') + "\Videos\MP4\Rotation_and_Detection.mp41111")

    # Exit if video not opened.
    if not video.isOpened():
        video = cv2.VideoCapture(0)

    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()

    # Define an initial bounding box
    bbox = (287, 23, 86, 320)

    # Uncomment the line below to select a different bounding box
    #image = cv2.resize(frame,(450,800))
    bbox = cv2.selectROI(frame, False)
    #bbox = tuple([(np.shape(frame)[1]/450) * x for x in bbox])

    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)

    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break

        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker.update(frame)


        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 10, 1)
        else:
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255),2)

        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

        # Display result
        cv2.imshow("Tracking", frame)
        #cv2.namedWindow("Tracking", cv2.WINDOW_NORMAL)  # Create window with freedom of dimensions
        #cv2.resizeWindow('Tracking', 450,800)
        #cv2.imshow("Tracking", frame)  # Show image

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27: break