# -*- coding: utf-8 -*-
#main function code

import detect
import cds
import time
import sys
import wjson
import datetime
import cv2
import record

contourHuman = 1500 # 모션 감지 민감도 설정-사람 감지
contourSleep = 500 # 모션 감지 민감도 설정-수면 뒤척임 감지
cdsSetvalue = 500 #조도센서 설정값
timeValue = 0

#조도센서로 불이 꺼지는것을 감지하면 사람의 움직임을 감지
def humanDetection():
    global cdsSetvalue, contourHuman
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

        if cdsValue > cdsSetvalue: #조도센서로 불이 꺼진걸 감지하면 
            print('불이 꺼짐, 동작 감지 시작, 감지 민감도: %d' % contourHuman)
            print('irLed on')
            cds.irLedon(26)
            motionValue = detect.motionDetect(10, contourHuman, 1) #일정시간동안 움직임 감지
            if motionValue >= 3: 
                print('사람감지, 수면감지 시작')
                return True #수면 감지
            else:
                cds.irLedoff(26)
                print('사람없음')

#불이 꺼지고 사람이 움직이는 것이 감지되면 
#사람이 잠드는 평균 시간인 30분간 모션 감지를 하여 
#수면 감지 판별
def sleepDetection():
    global cdsSetvalue, timeValue, contourSleep
    sleepdetect = 0
    totaldetect = 0
    count = 0
    exitcount = 0
    sleepValue = humanDetection() #불이 꺼지고 사람이 움직이는 것을 감지
    if sleepValue == True: #수면에 드는 시간은 보통 30분 이므로 30분동안 사람이 있는지 감지
        time.sleep(15) #정확한 분석을 위한 딜레이 //--15초
        print('30분간 움직임 획수 측정 시작, ?30초간 측정 시작')
        while count <= 3: #30분간 움직임 횟수 측정 //--30번
            print('일정 시간동안 모션 감지->, 감지 민감도: %d' % contourSleep)
            sleepdetect = detect.motionDetect(60, contourSleep, 1)  #//--60초간 모션감지
            count += 1 #시간 조정 카운트

            if sleepdetect >= 2: #1분동안 움직임 감지되면
                totaldetect += 1
                exitcount = 0
                timeValue = time.time() #수면 시작 시간 기록
                print('움직임 %d회 감지' % totaldetect)
            else: #움직임이 없으면 exitcount +1
                exitcount += 1
                print('움직임 없음')
            light = cds.light(4)
            if light < cdsSetvalue: #방안 등이 켜져있는지 검사
                print('light on, 수면감지 실패')
                return False
            if exitcount >= 10: #10분동안 움직임이 없으면
                break

        if totaldetect >= 2: #30분간 2번의 움직임이 감지되고 그 후 10분동안 연속으로 움직임이 없으면
            print('수면 감지, 잠자는 사람 존재')
            return True
        elif totaldetect <= 1: #30분간 1번 이하의 움직임이 감지되면 수면 감지 실패, 잠자리에 사람이 없음
            print('수면 감지 실패, 사람 없음')
            return False


#수면 패턴 측정
def sleepPattern():
    global timeValue, contourSleep
    d = datetime.date.today()
    print('수면 기록 start, json형식')
    wjson.writejson(timeValue, d, 1, 1, 1) # 잠이 들기 시작할때 기록 저장
    currentTime = time.time()
    
    while True:

        detect.motionDetect(0, contourSleep, 1)
            

def main():
    sleepValue = False
    while True:
        sleepValue = sleepDetection() # 수면 감지
        if sleepValue == True:
            print('수면패턴 측정 시작')
            sleepPattern()

        elif sleepValue == False:
            print('수면 감지 재시작')


def irledon():
    cds.irLedon(26)
    cds.irLedon(19)
    cds.irLedon(5)
    cds.irLedon(0)

def irledoff():
    cds.irLedoff(26)
    cds.irLedoff(19)
    cds.irLedoff(5)
    cds.irLedoff(0)


while True:
    print('동작 모드 선택')
    a = input('(1: 수면 패턴 측정, 2: 동작 감지 구역 설정, 3: 동작감지 테스트, 4: 수면 데이터 수집, 0: 종료): ')
    if 1 == a:
        try:
            record.reset() #수면 기록 txt 리셋
            main()
        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            pass
    elif 2 == a:
        detect.motionDetect(0, 100000, 1)
    elif 3 == a:
        b = int(input('동작 감지 설정값 입력: '))
        print('테스트를 끝내려면 esc키를 누르세요')
        irledon()
        print('irLed on')
        detect.motionDetect(-1, b, 1)
        irledoff()
        print('irLed off')
        cds.clean()
    elif 4 == a:
        record.start()
    elif 0 == a:
        break
    else:
        print('다시 입력해 주세요')
