from base.servo import ServoBase
import time

class LeftArm(ServoBase):

    # 舵机
    servos = {
        "A": {
            "channel": 11,
            "initAngle": 150,
            "minAngle": 0,
            "maxAngle": 180
        },
        "B": {
            "channel": 10,
            "initAngle": 30,
            "minAngle": 0,
            "maxAngle": 180
        }
    }

    # 初始化舵机角度
    def angleInit(self):
        time.sleep(.5)
        for servoName, servo in self.servos.items():
            self.servoMove(servo["channel"], servo["initAngle"])

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

            if self.writeEvent.target == "LeftArm":
                data = self.selfWorkQueue.get()
                getattr(self, data["type"])(data["data"])

            self.writeEvent.clear()


    # 碰个拳
    def fistBump(self, *args):
        time.sleep(.5)
        # 抬手
        self.servoMove(self.servos["A"]["channel"], 70, 2)

        # 左右晃
        self.servoMove(self.servos["B"]["channel"], 0, 1)
        self.servoMove(self.servos["B"]["channel"], 50, 1)

        # 回正
        self.servoMove(self.servos["B"]["channel"], 10, 2)
        #
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
        self.servoMove(self.servos["A"]["channel"], 50, .2)

        # 继续抬手
        self.servoMove(self.servos["A"]["channel"], 30)
        self.servoMove(self.servos["A"]["channel"], 0, 2)

        # 回复原位
        self.angleInit()

    def wave(self, *args):
        self.servoMove(self.servos["A"]["channel"], 0, 2)
        # 左右晃
        self.servoMove(self.servos["B"]["channel"], 0, .2)
        self.servoMove(self.servos["B"]["channel"], 30, .2)
        self.servoMove(self.servos["B"]["channel"], 0, .2)
        self.servoMove(self.servos["B"]["channel"], 30, 2)

        # 回复原位
        self.angleInit()
