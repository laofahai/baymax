from base.servo import ServoBase
import time

class Head(ServoBase):

    # 舵机
    servos = {
        "A": {
            "channel": 4,
            "initAngle": 90,
            "minAngle": 20,
            "maxAngle": 150
        }
    }

    def angleInit(self):
        self.servoMove(self.servos["A"]["channel"], self.servos["A"]["initAngle"])

    def run(self):
        time.sleep(1)
        self.angleInit()
        while True:
            self.writeEvent.wait()

            if self.writeEvent.target == "Head":
                data = self.selfWorkQueue.get()
                getattr(self, data["type"])(data["data"])

            self.writeEvent.clear()

    # 转头
    def turn(self, angle = "front"):
        if angle == "front":
            self.angleInit()
        else:
            self.servoMove(self.servos["A"]["channel"], angle)

    # 摇头
    def shake(self, times = 2):
        print(times)
        if not times:
            times = 3
        print(times)
        for i in range(times):
            self.servoMove(self.servos["A"]["channel"], self.servos["A"]["minAngle"], .2)
            self.servoMove(self.servos["A"]["channel"], self.servos["A"]["maxAngle"], .2)

        self.angleInit()



