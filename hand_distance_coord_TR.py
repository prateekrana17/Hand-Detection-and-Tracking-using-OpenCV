import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np

# Camera1

cam1 = cv2.VideoCapture(1)
cam1.set(3, 1280)
cam1.set(4, 720)

# Detector
hand_detector = HandDetector(detectionCon=0.8, maxHands=1)

# Generating a function for the relation x is the raw distance, y is the distance in cm
x = [457, 388, 368, 314, 290, 272, 251, 221, 204, 192, 175, 163, 156, 149, 136]
y = [30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y, 2)
# y = Ax^2 + Bx + C

# Loop
while True:
    success, img = cam1.read()
    hands, img = hand_detector.findHands(img)

    if hands:
        my_list = hands[0]['lmList']
        x, y, w, h = hands[0]['bbox']
        x1, y1 = my_list[5][:2]
        x2, y2 = my_list[17][:2]

        # Horizontal distance
        s = abs(x2 - x1)
        # Vertical distance
        k = abs(y2 - y1)
        # Diagonal distance
        d = int(math.sqrt(s ** 2 + h ** 2))
        # Distance in cm
        A, B, C = coff
        distanceCM = int(A * (d ** 2) + B * d + C)

        cvzone.putTextRect(img, f'{distanceCM} cm', (x + 5, y - 10))
        #cvzone.putTextRect(img, f'{x}, {y}')
        # Position
        print("Co-ordinates of the hand detected: ")
        print((x, y), (x+w, y), (x, y+h), (x+w, y+h))



    cv2.imshow("Camera 1", img)
    cv2.waitKey(1)