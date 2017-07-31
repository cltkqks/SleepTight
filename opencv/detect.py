#수면 감지 모듈

import RPi.GPIO as GPIO
import time

#조도센서 값을 읽어오는 함수
#빛이 있으면 300, 어두워지면 1000 이상을 리턴
def light(pin):
    count = 0

    #Output
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)

    #input으로 변환
    GPIO.setup(pin, GPIO.IN)

    #pin이 hign가 될때까지 카운트
    while (GPIO.input(pin) == GPIO.LOW):
        count += 1

    return count


