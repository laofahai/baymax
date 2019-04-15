try:
    import RPi.GPIO as GPIO
except:
    pass

import time

# 闪烁
def blink(channel, interval = .5, times = True):
    GPIO.setup(channel, GPIO.OUT)

    while times is True or times > 0:
        GPIO.output(channel, GPIO.HIGH)
        time.sleep(interval)
        GPIO.output(channel, GPIO.LOW)
        time.sleep(interval)

        if times is not True:
            times -= 1


# 关灯
def close(channel):
    GPIO.setup(channel, GPIO.OUT)
    GPIO.output(channel, GPIO.LOW)

# 开灯
def open(channel, continuedTime = True):
    GPIO.setup(channel, GPIO.OUT)
    GPIO.output(channel, GPIO.HIGH)
    if continuedTime is not True:
        time.sleep(continuedTime)
        GPIO.output(channel, GPIO.LOW)
