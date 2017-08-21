# -*- coding: utf-8 -*-
#수면 패턴 분석을 위한 기록 코드

import detect
import time
import sys

f = open("sleep.txt", 'w')
f.close()

def writetxt(contour):
    currentTime = time.time() #현재시간 구하기
    totalseconds = int(currentTime) #현재시간을 초 단위로 변환
    currentsecond = totalseconds % 60 #현재 시간의 초 구하기
    totalMinutes = totalseconds // 60 #현재시간을 분으로 변환
    currentMinute = totalMinutes % 60 #현재 시간의 분 구하기
    totalHours = totalMinutes // 60 # 현재 흐른시간을 시간으로 변환
    currentHour = totalHours % 24 # 현재시간의 시 구하기
    currentHour += 9 #한국시간으로 변화
    
    f = open("sleep.txt", 'a')
    data = "%d:%d contour값: %d\n" % (currentHour, currentMinute, contour)
    f.write(data)
    f.close()    
    




def main():
    print('수면 패턴 분석을 위한 기록 시작')
    while True:
        print('동작 감지중')
        area = detect.motionDetect(0, 10000)
        print('동작 감지됨, 정보 기록')
        writetxt(area)
        

try:
    main()
except KeyboardInterrupt:
    sys.exit()
