import threading
from utils.sound import Sound
from utils.client.baidu import Baidu
from base.organ import OrganBase
import time
import random

class Mouth(OrganBase):

    def run(self):
        while True:
            self.writeEvent.wait()
            if self.writeEvent.target == "Mouth":

                # 取出队列所有
                for i in range(1, self.selfWorkQueue.qsize()):
                    data = self.selfWorkQueue.get()
                    if "data" in data:
                        getattr(self, data["type"])(data["data"])
                    else:
                        getattr(self, data["type"])()

            self.writeEvent.clear()

    def speak(self, words):
        voicePath = Baidu.text2voice(words, "machine/machine_" + str(random.randint(1, 50)))
        Sound.play(voicePath)

    def sing(self, config):
        print("Mouth is singing: ", config["keyword"])
        Sound.playSong(config["keyword"], config["source"])

    def pause(self, *arg):
        Sound.pause()

    def unpause(self, *arg):
        Sound.unpause()

    def singPrevious(self, *arg):
        Sound.playPrevious()

    def singNext(self, *arg):
        Sound.playNext()

    def shutup(self, *arg):
        Sound.stop()

    def replayCurrent(self, *arg):
        Sound.replayCurrent()
