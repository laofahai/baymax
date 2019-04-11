# coding: utf-8
import importlib
import queue
import time
import abilities.intentions

from utils.servo import ServoControl
from utils import scaffolds
from organs.brain import Brain
from base.event import EventBase

class Baymax:

    # 器官实例列表
    organs = {}
    # 大脑
    brain = None

    # 器官工作队列
    workQueues = {}

    # 是否休眠状态
    sleeping = True

    def __init__(self):
        self.readEvent = EventBase()
        self.writeEvent = EventBase()
        self.workQueues["Brain"] = queue.Queue()

        organs = scaffolds.get_modules("organs")
        for organName in organs:
            if organName == ".brain" or organName == ".abilities" :
                continue

            organModule = importlib.import_module(organName, "organs")
            organClass = organName.replace(".", "")
            organClass = organClass[0].upper() + organClass[1:]

            if organClass in self.organs:
                continue

            if not organClass.startswith("__"):
                organ = getattr(organModule, organClass)
                self.workQueues[organClass] = queue.Queue()
                self.organs[organClass] = organ(
                    self.workQueues["Brain"],
                    self.workQueues[organClass],
                    self.writeEvent,
                    self.readEvent)
                self.organs[organClass].setName(organClass)
                self.organs[organClass].start()

        # 大脑单独启动
        if self.brain is None:
            self.brain = Brain(self, self.workQueues, self.writeEvent, self.readEvent)
            self.brain.start()


    def wakeup(self):
        self.organs["Mouth"].speak("你好，我是大白，是你的私人健康顾问")
        self.sleeping = False

    # @todo 休眠后 除大脑和耳朵之外 所有器官是否需要进入休眠
    def sleep(self):
        self.sleeping = True

        # for organ, organObject in self.organs.items():
        #     if organ == "Brain" or organ == "Ears":
        #         continue
        #
        #     organObject.join()
        #
        #     self.organs.pop(organ)
        #     self.workQueues.pop(organ)
        #
        # print(self.organs, self.workQueues)

    def isSleeping(self):
        return self.sleeping

if __name__ == "__main__":

    # ServoControl.moveToAngle(15, 0)
    # ServoControl.moveToAngle(15, 180)
    # ServoControl.moveToAngle(15, 0)
    # ServoControl.moveToAngle(15, 180)
    # ServoControl.moveToAngle(15, 0)
    #
    # ServoControl.moveToAngle(14, 0)
    # ServoControl.moveToAngle(14, 180)
    # ServoControl.moveToAngle(14, 0)
    # ServoControl.moveToAngle(14, 180)
    # ServoControl.moveToAngle(14, 0)
    #
    # ServoControl.moveToAngle(13, 0)
    # ServoControl.moveToAngle(13, 180)
    # ServoControl.moveToAngle(13, 0)
    # ServoControl.moveToAngle(13, 180)
    # ServoControl.moveToAngle(13, 0)

    baymax = Baymax()
    baymax.wakeup()

    # time.sleep(5)
    # baymax.brain.thinkAboutSentence("碰个拳")
    #
    # time.sleep(10)
    #
    # baymax.brain.thinkAboutSentence("我想听故事")

    while True:
        pass

    # baymax.brain.thinkAboutSentence("我想听杨超越的卡路里")



    # from utils.songDownloader import SongDownloader
    # from utils.sound import Sound
    #
    # Sound.playSong("卡路里")
    #
    # time.sleep(2)
    # Sound.pause()
    #
    # time.sleep(2)
    # Sound.unpause()
    #
    # time.sleep(2)
    # Sound.playNext()
    #
    # time.sleep(2)
    # Sound.playPrevious()
    #
    # time.sleep(2)
    # Sound.stop()

