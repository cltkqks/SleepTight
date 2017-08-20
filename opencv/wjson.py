# -*- coding: utf-8 -*-
#json 작성 코드

import json
import time
import datetime

def writejson(oldtime, d, sleeppattern, start_end, number): #함수 인자 oldtime(이전시간), day(날짜), sleeppattern(깊은잠 or 얕은잠), start_end, number(파일이름 넘버링)
        
    #지난 시간 구하기
    currentoldTime = oldtime #지난시간 구하기
    totaloldseconds = int(currentoldTime) #지난시간을 초 단위로 변환
    currentoldsecond = totaloldseconds % 60 #지난 시간의 초 구하기
    totaloldMinutes = totaloldseconds // 60 #지난시간을 분으로 변환
    currentoldMinute = totaloldMinutes % 60 #지난 시간의 분 구하기
    totaloldHours = totaloldMinutes // 60 # 지난 흐른시간을 시간으로 변환
    currentoldHour = totaloldHours % 24 # 지난시간의 시 구하기
    currentoldHour += 9 #한국시간으로 변화



    #현재 시간 구하기
    currentTime = time.time() #현재시간 구하기
    totalseconds = int(currentTime) #현재시간을 초 단위로 변환
    currentsecond = totalseconds % 60 #현재 시간의 초 구하기
    totalMinutes = totalseconds // 60 #현재시간을 분으로 변환
    currentMinute = totalMinutes % 60 #현재 시간의 분 구하기
    totalHours = totalMinutes // 60 # 현재 흐른시간을 시간으로 변환
    currentHour = totalHours % 24 # 현재시간의 시 구하기
    currentHour += 9 #한국시간으로 변화
    #print('Hour',currentHour, "Minute",currentMinute, "Second",currentsecond)
    
    #현재날짜 구하기
    #d = datetime.date.today() #한번만 실행 하면 되기에 
    
    name = str(number) + d.strftime('%Y%m%d') + '.json'

    day = int(d.strftime('%Y%m%d'))
    sleeptime = (currentoldHour*100) +  currentoldMinute
    patterntime = totalMinutes - totaloldMinutes
    print('filename: ' + name)
    print('day: %d ' % day)
    print('sleeptime: %d' %sleeptime)
    print('sleeppattern: %d' % sleeppattern)
    print('start_end: %d' % start_end)
    print('patterntime: %d' % patterntime)
    
    sleepData = {
        'day' : day,
        'sleeptime' : sleeptime,
        'sleeppattern' : sleeppattern,
        'start_end' : start_end,
        'patterntime' : patterntime
    }

    jsonString = json.dumps(sleepData)

    print('\njsonString')
    print(jsonString)

    with open(name, 'w') as make_file:
        json.dump(sleepData, make_file, ensure_ascii=False)    


writejson(time.time(), datetime.date.today(), 1, 1, 7)

