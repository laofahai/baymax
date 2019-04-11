from __future__ import division
import time

try:
    import Adafruit_PCA9685
except:
    pass


# 舵机控制
class ServoControl:

    inited = False

    pwm = None

    pulse_length = None

    @staticmethod
    def init():
        if ServoControl.inited:
            return
        ServoControl.inited = True
        # ServoControl.pulse_length = 1000000 // 50 // 4096
        ServoControl.pulse_length = 4
        ServoControl.pwm = Adafruit_PCA9685.PCA9685()
        ServoControl.pwm.set_pwm_freq(60)

    @staticmethod
    def setServoPulse(channel, pulse, timeSleep = 1):
        ServoControl.init()
        # pulse_length = 1000000    # 1,000,000 us per second
        # pulse_length //= 60       # 60 Hz
        # print('{0}us per period'.format(pulse_length))
        # pulse_length //= 4096     # 12 bits of resolution
        # print('{0}us per bit'.format(pulse_length))
        # pulse *= 1000
        # pulse //= ServoControl.pulse_length
        pulse //= 1
        ServoControl.pwm.set_pwm(channel, 0, pulse)

        if timeSleep > 0:
            time.sleep(timeSleep)

    @staticmethod
    def moveToAngle(channel, angle, timeSleep = 1):
        pulse = int(angle * 2.5 + 150)

        print("Servo {0} is moving to : angle( {1} ), pulse( {2} )".format(channel, angle, pulse))

        ServoControl.setServoPulse(channel, pulse, timeSleep = timeSleep)
