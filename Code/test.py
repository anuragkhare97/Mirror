import cv2
import numpy as np
import math


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
    #mask = cv2.dilate(mask,kernel)
    mask = cv2.GaussianBlur(mask,(5,5),100)
    getContours(mask,imgResult)
    cv2.imshow('img', mask)

def getContours(img,imgContour):
    try:
        contours,hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 5000:
                cv2.drawContours(imgResult, cnt, -1, (255,0,0),3)
                peri = cv2.arcLength(cnt, True)
                epsilon = 0.0005*cv2.arcLength(cnt,True)
                approx = cv2.approxPolyDP(cnt, 0.02*peri,True)
                x,y,w,h = cv2.boundingRect(approx)
                cv2.rectangle(imgContour, (x,y),(x+w,y+h),(0,255,0),5)
                # cv2.putText(imgContour, "Points: " + str(len(approx)), (x+w + 20,y+20), cv2.FONT_HERSHEY_COMPLEX,0.7,
                #             (0,255,0),2)
                hull = cv2.convexHull(cnt)

                areahull = cv2.contourArea(hull)
                areacnt = cv2.contourArea(cnt)

                arearatio = ((areahull-areacnt)/areacnt)*100

                l = 0

                hull = cv2.convexHull(approx, returnPoints = False)
                defects = cv2.convexityDefects(approx, hull)
                for i in range(defects.shape[0]):
                    s,e,f,d = defects[i,0]
                    start = tuple(approx[s][0])
                    end = tuple(approx[e][0])
                    far = tuple(approx[f][0])

                    a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                    b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                    c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                    s = (a + b + c) / 2
                    ar = math.sqrt(s * (s - a) * (s - b) * (s - c))

                    d = (2*ar)/a

                    angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57

                    if angle <= 90:
                        l += 1
                        cv2.circle(imgResult, far, 3, [0, 0, 255], -1)

                    if angle >= 90:
                        cv2.circle(imgResult, far, 3, [0, 0, 255], -1)
                        cv2.circle(imgResult, start, 3, [0, 0, 255], -1)
                        cv2.circle(imgResult, end, 3, [0, 0, 255], -1)


                    cv2.line(imgResult,start,end,[0,255,0],2)

                # if len(approx) == 11 or len(approx) == 12 or len(approx) == 13:
                #     cv2.putText(imgContour, "Five Fingers", (x + w + 20, y + 70), cv2.FONT_HERSHEY_COMPLEX,
                #                 0.7,
                #                 (0, 255, 0), 2)
                # elif len(approx) == 9 or len(approx) == 10:
                #     cv2.putText(imgContour, "Four Fingers", (x + w + 20, y + 70), cv2.FONT_HERSHEY_COMPLEX,
                #                 0.7,
                #                 (0, 255, 0), 2)
                # elif len(approx) == 7:
                #     cv2.putText(imgContour, "Three Fingers", (x + w + 20, y + 70), cv2.FONT_HERSHEY_COMPLEX,
                #                 0.7,
                #                 (0, 255, 0), 2)
                # elif len(approx) == 6:
                #     cv2.putText(imgContour, "One Finger", (x + w + 20, y + 70), cv2.FONT_HERSHEY_COMPLEX,
                #                 0.7,
                #                 (0, 255, 0), 2)
                # cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                #             (0, 255, 0), 2)
                # a = 0
                # while a < len(approx):
                #     if a == 11 or a == 8:
                #         cv2.circle(imgResult,([approx][0][a][0][0],[approx][0][a][0][1]),10,(0,0,255),cv2.FILLED)
                #
                #     a = a+1
                #cv2.drawContours(imgResult, [approx], -1, (0, 0, 255), 3)
                #cv2.line(imgResult,([approx][0][10][0][0],[approx][0][10][0][1]), ([approx][0][0][0][0],[approx][0][0][0][1]),(0,0,255),3)
                #print([approx][0][2][0][0])
                #cv2.circle(imgResult, ([approx][0][2][0][0], [approx][0][2][0][1]), 10, (0, 0, 255), cv2.FILLED)
    except:
        pass


while True:
    success, img = cap.read()
    imgResult = img.copy()
    #img = cv2.flip(img,1)
    kernel = np.ones((3,3),np.uint8)
    findColor(img)
    cv2.imshow("Result",imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
