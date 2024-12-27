import cv2
import time
import os
from CVZoneModule import HandDetector


################################################################
wCam, hCam = 1280, 740
################################################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0
listImage = os.listdir('image')
overlayList = []

for show in listImage:
    image = cv2.imread(f'image/{show}')

    overlayList.append(image)

detector = HandDetector(detectionCon=0.75)

fingers_up = 0

true_h = 0

for i in range(1,5) :
    print(i)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime


    hands, img = detector.findHands(img, draw=True, flipType=False)

    h,w,c = overlayList[fingers_up].shape
    img[0:h, 0:w] = overlayList[fingers_up]

    fps_size, _ = cv2.getTextSize(str(int(fps)),cv2.FONT_HERSHEY_PLAIN, 2, 2)
    cv2.putText(img, str(int(fps)), (w + 20,50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

    if hands :
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 landmarks for the first hand
        bbox1 = hand1["bbox"]  # Bounding box around the first hand (x,y,w,h coordinates)
        center1 = hand1['center']  # Center coordinates of the first hand
        handType1 = hand1["type"]  # Type of the first hand ("Left" or "Right")

        def findFingerHeight(p1,p2) :
            tr_h = 0
            for i in range(p1, p2) :
                l, _, _ = detector.findDistance(lmList1[i][0:2], lmList1[(i+1)][0:2],img=img,)
                tr_h += l
            return int(tr_h)

        len1, _ ,img = detector.findDistance(lmList1[5][0:2], lmList1[8][0:2],img=img, draw=True)

        thumb_lenght = findFingerHeight(5,8)
        prcnt = int(len1/thumb_lenght * 100)
        print(prcnt)

        fingers = detector.fingersUp(hand1)
        fingers_up = fingers.count(1)
        
    else :
        fingers_up = 0

    cv2.imshow("Finger Counter", img)
    cv2.waitKey(1)