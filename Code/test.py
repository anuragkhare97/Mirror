import cv2
import numpy as np


frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(10,130)




def findColor(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 20, 70])
    upper = np.array([20, 255, 255])
    mask = cv2.inRange(imgHSV, lower, upper)
    x,y=getContours(mask,imgResult)
    cv2.imshow('img', mask)

def getContours(img,imgContour):
    contours,hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:
            cv2.drawContours(imgResult, cnt, -1, (255,0,0),3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri,True)
            x,y,w,h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x,y),(x+w,y+h),(0,255,0),5)
            cv2.putText(imgContour, "Points: " + str(len(approx)), (x+w + 20,y+20), cv2.FONT_HERSHEY_COMPLEX,0.7,
                        (0,255,0),2)
            if len(approx) == 12 or len(approx) == 13:
                cv2.putText(imgContour, "Five Fingers", (x + w + 20, y + 70), cv2.FONT_HERSHEY_COMPLEX,
                            0.7,
                            (0, 255, 0), 2)
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)
            cv2.drawContours(imgResult, [approx], -1, (0, 0, 255), 3)
    return x+w//2,y


while True:
    success, img = cap.read()
    imgResult = img.copy()
    #img = cv2.flip(img,1)
    kernel = np.ones((3,3),np.uint8)
    findColor(img)
    cv2.imshow("Result",imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
