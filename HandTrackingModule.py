import cv2
import mediapipe as mp
import time

# cap = cv2.VideoCapture(0)

# mpHands = mp.solutions.hands
# hands = mpHands.Hands()
# mpDraw = mp.solutions.drawing_utils

# pTime = 0
# cTime = 0



#     cTime = time.time()
#     fps = 1/(cTime-pTime)
#     pTime = cTime

#     cv2.putText(fliped, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

#     cv2.imshow('image capture', fliped)
#     cv2.waitKey(1)

class handsDetector():
    def __init__(self, mode=False, maxHands=2, detectCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectCon = detectCon
        self.trackCon = trackCon
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,1,self.detectCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, isDraw=True):
        imgRgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.result = self.hands.process(imgRgb)
        # print(result.multi_hand_landmarks)

        # 1 for horizontal, 0 for vertical

        allHands = []
        h, w, c = img.shape
        if self.result.multi_hand_landmarks :
            for handType, handLms in zip(self.result.multi_handedness, self.result.multi_hand_landmarks) :
                
                if isDraw :
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self,img, handNo=0, isDraw=True):
        lms = []

        if self.result.multi_hand_landmarks :
            handLms = self.result.multi_hand_landmarks[handNo]

            clr = [(255,255,0), (255,0,255), (0, 255,255)]

            if handLms :
                for id, lm in enumerate(handLms.landmark) :
                    # print(id, lm)
                    h, w,c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    lms.append([id,cx,cy])
                    if isDraw:
                        if id == 8 :
                            cv2.putText(img, 'nice', (cx, cy), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

        def findDot(id=0, isDraw=True) :
            if self.result.multi_hand_landmarks :
                if len(lms) >= (id+1) :
                    id, cx, cy = lms[id]
                    print(id, cx,cy)

                    if isDraw :
                        cv2.circle(img, (cx,cy), 10, clr[handNo % len(clr)], cv2.FILLED)
                    return lms[id]
        return [lms, findDot]

def main() :
    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)
    detector = handsDetector()
    

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmsResult, findDot = detector.findPosition(img)

            
        findDot(4)

        # if detector.result.multi_hand_landmarks:
        #     for index, handLms in enumerate(detector.result.multi_hand_landmarks) :
                
        #         lmsResult = detector.findPosition(img, index)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

        cv2.imshow('image capture', img)
        cv2.waitKey(1)


if __name__ == '__main__' :
    main()