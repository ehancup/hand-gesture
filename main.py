import cv2
import mediapipe as mp
import time
import math
import numpy as np
from HandTrackingModule import handsDetector
from CVZoneModule import HandDetector
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui
import threading
import keyboard
from PIL import Image
import os

################################################################
wCam, hCam = 640, 480
################################################################


pTime = 0
cTime = 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = HandDetector()
# detector = handsDetector()

def countDistance(thumb, nail) : return int(math.sqrt((nail[1] - thumb[1])**2 + (nail[2] - thumb[2])**2))
def textPosition(thumb, nail) :
    middle_x = int((thumb[0] + nail[0]) / 2)
    middle_y = int((thumb[1] + nail[1]) / 2)

    return (middle_x, middle_y)

def textOriginCenter(canvas, text) :
    return (int(canvas[0]) - (text[0] // 2), int(canvas[1]) + (text[1] // 2))

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
minVol , maxVol,  _ = volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(0, None)  

#################################
space_pressed_time = 0
down_pressed_time = 0
rl_pressed_time = 0
ss_pressed_time = 0
#################################


def press_space():
    keyboard.press_and_release('space')
def press_down():
    keyboard.press_and_release('down')
def screen_shot():
    dir_exist = os.path.exists('ss/')
    if not dir_exist: os.mkdir('ss/')
    file_index = 0
    while True:
        is_exist = os.path.exists(fr'ss/photo_{file_index}.png')
        if is_exist:
            file_index = file_index + 1
        else:
            break
    mySC = pyautogui.screenshot()
    mySC.save(rf'ss/photo_{file_index}.png')
    img = Image.open(rf'ss/photo_{file_index}.png')
    img.show()


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, draw=True, flipType=False)
    # lmsResult, findFinger = detector.findPosition(img, isDraw=False)
    # lmsResult2, findFinger2 = detector.findPosition(img, isDraw=False, handNo=1)

    
    # thumb = findFinger(4)  
    # thumb2 = findFinger2(4)  
    # nail = findFinger(12)
    # mini = findFinger(20)


        # if detector.result.multi_hand_landmarks:
        #     for index, handLms in enumerate(detector.result.multi_hand_landmarks) :

        #         lmsResult = detector.findPosition(img, index)   

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    if hands :
        # textSpasiPos = textPosition(thumb=thumb, nail=nail)
        # textDownPos = textPosition(thumb=thumb, nail=mini)
        # jarakSpasi = countDistance(thumb, nail)  
        # jarakDown = countDistance(thumb, mini)
        # if jarakSpasi < 30 :
        #     pyautogui.press('space')
        #     time.sleep(1)

        # if jarakDown < 30 :
        #     pyautogui.press('down')
        #     # time.sleep(1)
        # cv2.putText(img, str(jarakDown), textDownPos, cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 landmarks for the first hand
        bbox1 = hand1["bbox"]  # Bounding box around the first hand (x,y,w,h coordinates)
        center1 = hand1['center']  # Center coordinates of the first hand
        handType1 = hand1["type"]  # Type of the first hand ("Left" or "Right")

        


        spaceLen, _, img = detector.findDistance(lmList1[4][0:2], lmList1[12][0:2], img, color=(255, 255,0),scale=10)
        downLen, _, img = detector.findDistance(lmList1[4][0:2], lmList1[16][0:2], img, color=(255, 255,0),scale=10)
        rlLen, _, img = detector.findDistance(lmList1[4][0:2], lmList1[16][0:2], img, color=(255, 255,0),scale=10)

        if spaceLen < 30 and (time.time() - space_pressed_time > 1) :
            text_size, _ = cv2.getTextSize("SPACE", cv2.FONT_HERSHEY_DUPLEX, 2, 2)
            cv2.putText(img, "SPACE", (640//2 - text_size[0] //2, 480//2 + text_size[1] //2), cv2.FONT_HERSHEY_DUPLEX, 2, (255,0,0), 2, cv2.LINE_AA) # type: ignore
            
            threading.Thread(target=press_space).start()
            space_pressed_time = time.time()      

        if downLen < 25 and (time.time() - down_pressed_time > 1) :
            text_size2, _ = cv2.getTextSize("DOWN", cv2.FONT_HERSHEY_DUPLEX, 2, 2)
            cv2.putText(img, "DOWN", (640//2 - text_size2[0] //2, 480//2 + text_size2[1] //2), cv2.FONT_HERSHEY_DUPLEX, 2, (255,0,0), 2, cv2.LINE_AA) # type: ignore

            threading.Thread(target=press_down).start()
            down_pressed_time = time.time()
        

        if len(hands) == 2 :
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # List of 21 landmarks for the first hand
            bbox2 = hand2["bbox"]  # Boundi ng box around the first hand (x,y,w,h coordinates)
            center2 = hand2['center']  # Center coordinates of the first hand
            handType2 = hand2["type"]

            betweenLen, _, img = detector.findDistance(lmList1[8][0:2], lmList2[8][0:2], img, color=(255, 255,0),scale=10)
            length, _, img = detector.findDistance(lmList2[8][0:2], lmList1[8][0:2], img, color=(255, 255,0),scale=10)
            length1, _, img = detector.findDistance(lmList2[4][0:2], lmList2[8][0:2], img, color=(0, 255,255),scale=10)
            length2, _, img = detector.findDistance(lmList1[4][0:2], lmList1[8][0:2], img, color=(0, 255,255),scale=10)

            ss_length1, _, img = detector.findDistance(lmList1[4][0:2], lmList2[8][0:2], img, color=(0, 255,255),scale=10, draw=True)
            ss_length2, _, img = detector.findDistance(lmList2[4][0:2], lmList1[8][0:2], img, color=(255, 0,255),scale=10, draw=True)


            if betweenLen < 10 and (time.time() - down_pressed_time > 1) :
                text_size2, _ = cv2.getTextSize("DOWN", cv2.FONT_HERSHEY_DUPLEX, 2, 2)
                cv2.putText(img, "DOWN", (640//2 - text_size2[0] //2, 480//2 + text_size2[1] //2), cv2.FONT_HERSHEY_DUPLEX, 2, (255,0,0), 2, cv2.LINE_AA)# type: ignore

                threading.Thread(target=press_down).start()
                down_pressed_time = time.time()

            if ss_length1 < 40 and ss_length2 < 40 and (time.time() - ss_pressed_time > 1) :
                text_size2, _ = cv2.getTextSize("screen shot", cv2.FONT_HERSHEY_DUPLEX, 2, 2)
                cv2.putText(img, "scree shot", (640//2 - text_size2[0] //2, 480//2 + text_size2[1] //2), cv2.FONT_HERSHEY_DUPLEX, 2, (255,0,0), 2, cv2.LINE_AA)# type: ignore

                threading.Thread(target=screen_shot).start()
                ss_pressed_time = time.time()

            
        # volume.SetMasterVolumeLevel(vol, None)  

        # if length < 30 :
        #     pyautogui.press('space')

            position = textPosition(lmList2[8][0:2], lmList1[8][0:2])
            position1 = textPosition(lmList2[4][0:2], lmList2[8][0:2])
            position2 = textPosition(lmList1[4][0:2], lmList1[8][0:2])
        
            cx , cy = lmList1[4][0:2]
            # cv2.putText(img, str(int(length)), position, cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 2)
            # cv2.putText(img, str(int(length1)), position1, cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)
            # cv2.putText(img, str(int(length2)), position2, cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)
            if int(length1) < 30 and int(length2) < 30 :
                vol = np.interp(length, [100, 400], [-80.0, maxVol])
                volPer = np.interp(length, [100, 400], [0, 100])
                volume.SetMasterVolumeLevel(vol, None)  

                TEXT_FACE = cv2.FONT_HERSHEY_DUPLEX
                TEXT_SCALE = 1
                TEXT_THICKNESS = 1
                TEXT = f"{int(volPer)}%"

                text_size, _ = cv2.getTextSize(TEXT, TEXT_FACE, TEXT_SCALE, TEXT_THICKNESS)
                text_origin = (position[0] - text_size[0] // 2, position[1] + text_size[1] // 2)

                cv2.circle(img, position, 40, (127,0,127), cv2.FILLED) # type: ignore
                cv2.putText(img, TEXT, text_origin, TEXT_FACE, TEXT_SCALE, (127,255,127), TEXT_THICKNESS, cv2.LINE_AA) # type: ignore

    cv2.imshow('image capture', img) # type: ignore
    cv2.waitKey(1)
