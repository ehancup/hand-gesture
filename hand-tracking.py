import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()

    fliped = cv2.flip(img, 1)
    imgRgb = cv2.cvtColor(fliped, cv2.COLOR_BGR2RGB)

    result = hands.process(imgRgb)
    # print(result.multi_hand_landmarks)

    # 1 for horizontal, 0 for vertical

    if result.multi_hand_landmarks :
        for handLms in result.multi_hand_landmarks :
            for id, lm in enumerate(handLms.landmark) :
                # print(id, lm)
                h, w,c = fliped.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id, cx, cy)
                if id == 8 :
                    cv2.putText(fliped, 'nice', (cx, cy), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
            mpDraw.draw_landmarks(fliped, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(fliped, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    cv2.imshow('image capture', fliped)
    cv2.waitKey(1)