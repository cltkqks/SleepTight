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

fps = 10  #fps값 설정 변수
cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, fps) # fps 설정
cap.set(3,640) #width 설정
cap.set(4,480) #heigth 설정

mog = cv2.createBackgroundSubtractorMOG2()   #차영상을 구하기위한 함수 설정
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))  #노이즈 제거를 위한 커널 설정

def onMouse(event, x, y, flags, param): #마우스 동작 함수 roi 선택용
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
            height, width = abs(y-row), abs(x-col)
            trackWindow = (col,row,width,height)
            sp = open('savePoint.txt','w')
            a = [str(col), str(row),str(width), str(height)]
            sp.write('\n'.join(a))
            sp.close()
        return
        
def backSubtraction(roi):  # 차영상을 구해 리턴하는 함수
        
    fgmask = mog.apply(roi)   #배경제거
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)  #차영상의 노이즈 제거
    cv2.imshow('originalroi', roi) #roi 영상 확인용
    cv2.imshow('mask', fgmask)     #roi 내 차영상 
    return fgmask


def readFile():
    global col, row, width, height 
    try: #파일이 없어 오류 발생시 파일 생성
        f = open('savePoint.txt', 'r')
        col = int(f.readline())
        row = int(f.readline())
        width = int(f.readline())
        height = int(f.readline())
        f.close()
    except IOError: #IOError 오류가 생길때 파일 생성
        f = open('savePoint.txt', 'w')
        a = [str(1), str(1), str(1), str(1)]
        f.write('\n'.join(a))
        f.close()
        
        
#모션 감지 함수
#모션 감지 수행하는 시간을 time을 통해 조절할수 있고 
#모션감지함수를 시간제한없이 동작시키려면 time에 0을 넣어준다    
def motionDetect(time):
    global frame, frame2, inputmode, fps
    count = 0
    ret, frame = cap.read()
    readFile()
    cv2.rectangle(frame,(col,row),(col+width,row+height),(0,255,0),2)
    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', onMouse, param=(frame,frame2))
        

    while True:
        ret, frame = cap.read()
        roi = frame[row:row+height, col:col+width] #영상에서 선택한 영역이외는 자름
        if not ret:
            break

        fgmask = backSubtraction(roi)
        _, contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # contours를 찾는다
        count += 1
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

        if time != 0 and count >= fps*time: #모션감지 동작시간 time값이 0이면 계속 동작
            break

    cap.release()
    cv2.destroyAllWindows()



motionDetect(0)


