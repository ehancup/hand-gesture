import cv2
import time
import os
from CVZoneModule import HandDetector


################################################################
wCam, hCam = 640, 480
################################################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

listImage = os.listdir('image')
overlayList = []

for show in listImage:
    image = cv2.imread(f'image/{show}')

    overlayList.append(image)

detector = HandDetector(detectionCon=0.75)
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    h,w,c = overlayList[0].shape
    img[0:h, 0:w] = overlayList[0]

    cv2.imshow("Finger Counter", img)
    cv2.waitKey(1)