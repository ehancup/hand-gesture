import cv2
import numpy as np
import time
import os
from CVZoneModule import HandDetector

cap = cv2.VideoCapture(0)
folderPath = 'header'
myList = os.listdir(folderPath)
headerList = [cv2.imread(f'{folderPath}/{i}') for i in myList]
print(len(headerList))
detector = HandDetector(detectionCon=0.85)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    h, w, c = img.shape
    hh, hw, hc = headerList[0].shape
    headerH = int((w * hh) / hw)
    
    img[0:headerH, 0:w] = cv2.resize(headerList[0], (w, headerH), interpolation=cv2.INTER_AREA)

    # cv2.putText(img, str(w), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    # cv2.putText(img, str(h), (10, 140), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    hands, img = detector.findHands(img, draw=True, flipType=False)
    if hands :
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 landmarks for the first hand
        bbox1 = hand1["bbox"]  # Bounding box around the first hand (x,y,w,h coordinates)
        center1 = hand1['center']  # Center coordinates of the first hand
        handType1 = hand1["type"]  # Type of the first hand ("Left" or "Right")

        fingers = detector.fingersUp(hand1)
        print(fingers)

    cv2.imshow('image capture', img)
    cv2.waitKey(1)