from base.organ import OrganBase
from utils.servo import ServoControl

class ServoBase(OrganBase):

    def servoMove(self, channel, angle, timeSleep = .5):
        ServoControl.moveToAngle(channel, angle, timeSleep)

    # 初始化舵机角度
    def angleInit(self):
        for servoName, servo in self.servos.items():
            self.servoMove(servo["channel"], servo["initAngle"])


