# -*- coding: utf-8 -*-

import numpy as np
import cv2
import os
os.system('sudo modprobe bcm2835-v4l2')

col, width, row, height = -1, -1, -1, -1
frame = None
frame2 = None
inputmode = False
rectangle = False

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

mog = cv2.createBackgroundSubtractorMOG2()   #차영상을 구하기위한 함수 설정
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))  #노이즈 제거를 위한 커널 설정

def onMouse(event, x, y, flags, param):
        global col, width, row, height, frame, frame2, inputmode
        global rectangle

        if inputmode:
                if event==cv2.EVENT_LBUTTONDOWN:
                        rectangle = True
                        col,row = x,y
                elif event==cv2.EVENT_MOUSEMOVE:
                        if rectangle:
                                frame=frame2.copy()
                                cv2.rectangle(frame,(col,row),(x,y),(0,255,0),2)
                                cv2.imshow('frame', frame)
                elif event==cv2.EVENT_LBUTTONUP:
                        inputmode = False
                        rectangle = False
                        cv2.rectangle(frame,(col,row),(x,y),(0,255,0),2)
                        height, width = abs(row-y), abs(col-x)
                        trackWindow = (col,row,width,height)
                        sp = open('savePoint','w')
                        a = [str(col), str(row),str(x), str(y)]
                        sp.write('\n'.join(a))
                        sp.close()
                return
        
def backSubtraction(roi):  # 차영상을 구해 리턴하는 함수

    ret, roi = cap.read()  #ret: 프레임 캡쳐 결과, frame: 캡쳐한 프레임
    fgmask = mog.apply(roi)   #배경제거
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)  #차영상의 노이즈 제거
    cv2.imshow('mask', fgmask)
    return fgmask


def readFile():
        f = open('savePoint', 'r')
        col = int(f.readline())
        row = int(f.readline())
        width = int(f.readline())
        height = int(f.readline())
        f.close()
        
        
    
def motionDetect():
        global frame, frame2, inputmode
        ret, frame = cap.read()
        readFile()
        cv2.rectangle(frame,(col,row),(col+width,row+height),(0,255,0),2)
        cv2.namedWindow('frame')
        cv2.setMouseCallback('frame', onMouse, param=(frame,frame2))

        while True:
                ret, frame = cap.read()
                roi = frame[col:col+width,row:row+height]
                if not ret:
                        break
                if not os.path.exists('savePoint') or not os.path.getsize('savePoint') > 0:
                        inputmode = True
                        frame2 = frame.copy()

                        while inputmode:
                                cv2.imshow('frame1',frame)
                                cv2.waitKey(0)
                fgmask = backSubtraction(roi)
                _, contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # contours를 찾는다
      #          count += 1
                for c in contours: # 한 프레임의 contour들을 모두 찾아 검사해 움직임을 감지
                        if cv2.contourArea(c) < 10000:#범위: #일정한 크기이상의 contours가 없으면 아래는 무시하고 while루프를 돈다
                                continue
                        else :
                                print('MD')
                
                cv2.rectangle(frame,(col,row),(col+width,row+height),(0,255,0),2)
                cv2.imshow('frame', frame)
                k=cv2.waitKey(1)&0xFF
                if k==27:
                        break
                if k==ord('i'):
                        print('press any key to start detecting')
                        inputmode = True
                        frame2 = frame.copy()

                        while inputmode:
                                cv2.imshow('frame',frame)
                                cv2.waitKey(0)
        cap.release()
        cv2.destroyAllWindows()
motionDetect()


