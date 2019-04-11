import threading
from utils.recorder import Recorder
from base.organ import OrganBase
from utils.sound import Sound

class Ears(OrganBase):

    def run(self):
        self.listen()

    def listen(self):
        while True:
            Recorder.startRecord()
            self.notifyBrain({
                "type": "input",
                "organ": "Ears",
                "data": Recorder.savPath
            })
            # self.writeEvent.wait() #--> 等待写事件
            #
            # if self.writeEvent.target == "Ears":
            #     print("ears get command")

            # self.writeEvent.clear() #-->清除写事件，以方便下次读取
            # time.sleep(1)
