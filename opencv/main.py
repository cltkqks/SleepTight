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

contourHuman = 1000 # 모션 감지 민감도 설정-사람 감지
contourSleep = 400  # 모션 감지 민감도 설정-수면 뒤척임 감지
cdsSetvalue = 600 #조도센서 설정값
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
            irledon()
            i = 0
            while i < 2:
                areaValue = detect.motionDetect(100, contourHuman, 1) #일정시간동안 움직임 감지
                if areaValue > 0:
                    detectNumber += 1
                time.delay(1) #정확한 감지를 위한 딜레이
            if detectNumber >= 2: 
                print('사람감지, 수면감지 시작')
                return True #수면 감지
            else:
                irledoff()
                print('사람없음')

#불이 꺼지고 사람이 움직이는 것이 감지되면 
#사람이 잠드는 평균 시간인 30분간 모션 감지를 하여 
#수면 감지 판별
def sleepDetection():
    global cdsSetvalue, timeValue, contourSleep
    sleepdetect = 0
    totaldetect = 0
    count = 0
    cdsCount = 0 
    exitcount = 0

    sleepValue = humanDetection() #불이 꺼지고 사람이 움직이는 것을 감지

    if sleepValue == True: 
        time.sleep(3) #정확한 분석을 위한 딜레이 

        print('사람이 잠자는지 수면 감지 판별 start')
        while count < 10: #5분간 잠자는 공간을 모션 감지하여 사람이 진짜 잠자는지 판별
            print('일정시간 동안 움직임 감지')
            sleepdetect = detect.motionDetect(30, contourSleep, 1)
            if sleepdetect > 0: # 중복 감지를 방지하기 위한 딜레이
                time.delay(3) 
            count += 1

            if sleepdetect > 0: #움직임이 감지되면 참
                totaldetect += 1
            if totaldetect > 1:
                print('수면 중인 사람 감지 성공')
                return True
            while cdsCount < 3: 
                light = cds.light(4)
                print('조도 값: %d' % light)
                cdsCount += 1
            cdsCount = 0
            if light < cdsSetValue: #방안 등이 켜져있는지 검사
                print('light on, 수면 감지 실패')
                return False
        print('수면중인 사람 감지 실패, 사람 없음')
        return False
         


#수면 패턴 측정
def sleepPattern():
    global timeValue, contourSleep
    maximumArea = 0
    d = datetime.date.today()
    start_end = 1 #수면 시작, 끝 flag
    sleepPattern = 1 #수면패턴 정보, 시작은 얕은 잠
    timeFlag = 0 #시간 저장을 위한 flag
    writeIndex = 1 #json 파일 넘버 인덱스
    cdsCount = 0 # 조도센서 측정을 위한 


    print('수면 기록 start, json형식')
    startTime = time.time() #수면 시작 시간 기록
    
    while True:
        time1 = time.time() # time1, time2는 모션 감지 시간 간격을 재기 위한 변수
        areaValue = detect.motionDetect(0, contourSleep, 1)
        time2 = time.time()
        timeInterval = int(time2 - time1)

        if timeFlag == 0: #시간 저장을 위한 함수
            startTime = time1
            timeFlag = 1

        while cdsCount < 3:
            light = cds.light(4)
            print('조도 값: %d' % light)
            cdsCount += 1
        cdsCount = 0
        if light < cdsSetValue:
            print('light on, 수면 끝')
            




        if timeInterval < 5: #짧은 시간내에 여러번 모션 감지가 되면 가장 큰 값만 얻기 위해(시간간격 4초이내)
            if areaValue > maximumArea:
                maximumArea = areaValue
                      
        elif timeInterval > 840: #14분간 움직임이 없으면 깊은 수면
            #startTime == time1 이 참일때
            if startTime == time1:
                wjson.writejson(startTime, time2, d, 0, start_end, writeIndex)
                if start_end == 1:
                    start_end = 0
                writeIndex += 1
                timeFlag = 0

            #startTime 부터 time1 까지 얕은 수면
            else:
                wjson.writejson(startTime, time1, d, 1, start_end, writeIndex)
                if start_end == 1:
                    start_end = 0
                writeIndex += 1
                timeFlag = 0
                #time1 부터 time2까지 깊은 수면
                wjson.writejson(time1, time2, d, 0, start_end, writeIndex)
                writeIndex += 1       
        else:
            pass      


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
    cds.irLedon(14)


def irledoff():
    cds.irLedoff(14)


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
        c = input('irLed on(1), off(0) 선택')
        print('테스트를 끝내려면 esc키를 누르세요')
        if c == 1:
            irledon()
            print('irLed on')
        detect.motionDetect(-1, b, 1)
        if c == 1:
            irledoff()
            print('irLed off')
            cds.clean()
    elif 4 == a:
        record.start()
    elif 0 == a:
        break
    else:
        print('다시 입력해 주세요')
