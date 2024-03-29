from base.servo import ServoBase
import time

class RightArm(ServoBase):

    # 舵机
    servos = {
        "A": {
            "channel": 15,
            "initAngle": 30,
            "minAngle": 0,
            "maxAngle": 180
        },
        "B": {
            "channel": 14,
            "initAngle": 150,
            "minAngle": 0,
            "maxAngle": 180
        }
    }

    def run(self):
        self.angleInit()
        # ServoControl.moveToAngle(15, 0)
        # ServoControl.moveToAngle(15, 180)
        # ServoControl.moveToAngle(15, 0)
        # ServoControl.moveToAngle(15, 180)
        # ServoControl.moveToAngle(15, 0)
        # self.fistBump()
        while True:
            self.writeEvent.wait()

            if self.writeEvent.target == "RightArm":
                data = self.selfWorkQueue.get()
                getattr(self, data["type"])(data["data"])

            self.writeEvent.clear()


    # 碰个拳
    def fistBump(self, *args):
        # 抬手
        self.servoMove(self.servos["A"]["channel"], 110, 2)

        # 左右晃
        self.servoMove(self.servos["B"]["channel"], 180, 1)
        self.servoMove(self.servos["B"]["channel"], 140, 1)

        # 回正
        self.servoMove(self.servos["B"]["channel"], 160, 2)

        # # 翻手
        # self.servoMove(self.servos["C"]["channel"], 0)

        time.sleep(1)

        # 说话
        self.notifyBrain({
            "type": "control",
            "organ": "Mouth",
            "command": {
                "type": "speak",
                "data": " 把拉 辣了啊"
            }
        })

        # 继续抬手
        self.servoMove(self.servos["A"]["channel"], 125)

        # 继续抬手
        self.servoMove(self.servos["A"]["channel"], 145)
        self.servoMove(self.servos["A"]["channel"], 165, 2)

        # 回复原位
        self.angleInit()

    def shakeHand(self, *args):
        # 抬手
        self.servoMove(self.servos["A"]["channel"], 110, 2)

        # 上下晃
        self.servoMove(self.servos["A"]["channel"], 130, .5)
        self.servoMove(self.servos["A"]["channel"], 90, .5)
        self.servoMove(self.servos["A"]["channel"], 130, .5)
        self.servoMove(self.servos["A"]["channel"], 90, .5)

        self.servoMove(self.servos["A"]["channel"], 110, 3)

        self.angleInit()
