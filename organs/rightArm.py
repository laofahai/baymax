from base.arm import ArmBase
import time

class RightArm(ArmBase):

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
            "initAngle": 30,
            "minAngle": 0,
            "maxAngle": 60
        },
        "C": {
            "channel": 13,
            "initAngle": 45,
            "minAngle": 0,
            "maxAngle": 90
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

        # 左右晃 电机正
        # self.servoMove(self.servos["B"]["channel"], 10, 1)
        # self.servoMove(self.servos["B"]["channel"], 60)
        # 左右晃 电机反装
        self.servoMove(self.servos["B"]["channel"], 80, 1)
        self.servoMove(self.servos["B"]["channel"], 0, 1)

        # 回正
        self.servoMove(self.servos["B"]["channel"], self.servos["B"]["initAngle"])

        # 翻手
        self.servoMove(self.servos["C"]["channel"], 0)

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

        time.sleep(1)

        # 继续抬手
        self.servoMove(self.servos["A"]["channel"], 125, .2)

        # 继续抬手
        self.servoMove(self.servos["A"]["channel"], 135, .2)
        self.servoMove(self.servos["A"]["channel"], 145, .2)
        self.servoMove(self.servos["A"]["channel"], 155, .2)
        self.servoMove(self.servos["A"]["channel"], 165, 2)

        # 回复原位
        self.angleInit()
