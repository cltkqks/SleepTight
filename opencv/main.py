# -*- coding: utf-8 -*-
#main function code

import detect
import cds
import time
import sys

#조도센서로 불이 꺼지는것을 감지하면 사람의 움직임을 감지
def humanDetection():
    cdsValue = 0
    cdsCount = 0
    print('조도 센서 감지')
    while True:
        time.sleep(1)
        while cdsCount <= 2:
            cdsValue = cds.light(4)
            print(cdsValue)
            cdsCount += 1

        cdsCount = 0

        if cdsValue > 1000: #조도센서로 불이 꺼진걸 감지하면 
            print('불이 꺼짐, 동작 감지 시작')
            motionValue = detect.motionDetect(10) #일정시간동안 움직임 감지
            if motionValue >= 5:
                print('사람감지, 수면감지 시작')
                return True #수면 감지
            else:
                print('사람없음')

#불이 꺼지고 사람이 움직이는 것이 감지되면 
#사람이 잠드는 평균 시간인 30분간 모션 감지를 하여 
#수면 감지 판별
def sleepDetection():
    sleepdetect = 0
    totaldetect = 0
    count = 0
    exitcount = 0
    sleepValue = humanDetection() #불이 꺼지고 사람이 움직이는 것을 감지
    if sleepValue == True: #수면에 드는 시간은 보통 30분 이므로 30분동안 사람이 있는지 감지
        time.sleep(5) #정확한 분석을 위한 딜레이 //--60초

        print('30분간 움직임 획수 측정 시작, ?30초간 측정 시작')
        while count <= 3: #30분간 움직임 횟수 측정 //--30번
            print('일정 시간동안 모션 감지->')
            sleepdetect = detect.motionDetect(10)  #//--60초간 모션감지
            count += 1 #시간 조정 카운트

            if sleepdetect >= 3: #1분동안 움직임 감지되면
                totaldetect += 1
                exitcount = 0
                print('움직임 %d회 감지' % totaldetect)
            else: #움직임이 없으면 exitcount +1
                exitcount += 1
                print('움직임 없음')
            light = cds.light(4)
            if light < 1000:
                print('light on, 수면감지 실패')
                return False

        if totaldetect >= 1 and exitcount >= 0: #30분간 3번의 움직임이 감지되고 그 후 5분동안 연속으로 움직임이 없으면
            print('수면 감지, 잠자는 사람 존재')
            return True
        elif totaldetect < 1: #30분간 1번 이하의 움직임이 감지되면 수면 감지 실패, 잠자리에 사람이 없음
            print('수면 감지 실패, 사람 없음')
            return False


#수면 패턴 측정
def sleepPattern():
    sleepValue = sleepDetection() #수면 감지
    if sleepValue == True:
        print('수면 패턴 측정 시작')
        
    elif sleepValue == False:
        print('수면 감지 재시작')
        sleepPattern()

            

try:
    sleepPattern()
except KeyboardInterrupt:
    sys.exit()
