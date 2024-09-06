from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import numpy as np

# Parameters

gestureThreshold = 300
folderPath = "Presentation"

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


#presentation images
pathImages = os.listdir(folderPath)
#print(pathImages)

#Variables
imgNumber = 0
hs, ws = 120,213
gestureThreshold = 300
width = 500
height = 600
buttonPressed = False
buttonCounter = 0
buttonDelay = 30

# hand detector
detector = HandDetector(detectionCon=0.5, maxHands=1)

while True:
    #import images

    success,img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath,pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    hands, img= detector.findHands(img)
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx,cy = hand['center']
        lmList = hand['lmList']
        #constrait values

        indexFinger =lmList[8][0], lmList[8][1]
        #xVal = int(np.interp(lmList[8][0],[width // 2, ws],[0,width]))
        #yVal = int(np.interp(lmList[8][1], [150,height-150], [0, height]))
        #qindexFinger = xVal, yVal

        if cy <= gestureThreshold:
            if fingers == [1,0,0,0,0]:
                print("left")

                if imgNumber>0:
                    buttonPressed = True
                    imgNumber -= 1


            if fingers == [0,0,0,0,1]:
                print("right")
                if imgNumber < len(pathImages)-1:
                    buttonPressed = True
                    imgNumber += 1

        if fingers == [0,1,1,0,0]:
              cv2.circle(imgCurrent, indexFinger,12, (0,0,255), cv2.FILLED)

#button pressed
    if buttonPressed:
        buttonCounter +=1
        if buttonCounter> buttonDelay:
            buttonCounter = 0
            buttonPressed = False







    # adding webcam image on the slide
    imgSmall = cv2.resize(img,(ws, hs))
    h,w,_ = imgCurrent.shape
    imgCurrent[0:hs,w-ws:w] = imgSmall

    cv2.imshow('image',img)
    cv2.imshow("slides", imgCurrent)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break


