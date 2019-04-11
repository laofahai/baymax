# coding: utf-8

"""
大脑收到信号
eg: ears.listen -> brain.receiveSignal -> brain.resolveInput -> brain.thinkAbout -> brain.giveCommand -> organs.execute
"""
import importlib
import threading
from utils.client.baidu import Baidu
from utils.client.turing import Turing
from utils.client.unit import UNIT
from utils import scaffolds
from utils.sound import Sound
from abilities.sentence import wakeup

class Brain(threading.Thread):

    # 意图
    intentions = {}

    # 能力
    abilities = []

    def __init__(self, baymax, workQueues, writeEvent, readEvent):
        super().__init__()
        self.baymax = baymax
        self.workQueues = workQueues
        self.readEvent = readEvent
        self.writeEvent = writeEvent

        self.daemon = True

        # 意图分析
        intentions = scaffolds.get_modules("abilities/intentions")
        for intention in intentions:
            module = importlib.import_module(intention, "abilities.intentions")
            self.intentions[intention.replace(".", "")] = module

        # 本地自定义能力
        abilities = scaffolds.get_modules("abilities/sentence")
        for ability in abilities:
            if ability == ".wakeup":
                continue
            module = importlib.import_module(ability, "abilities.sentence")
            self.abilities.append(module)

    def run(self):
        while True:
            self.readEvent.wait()
            data = self.workQueues["Brain"].get()
            getattr(self, data["type"] + "With" + data["organ"])(data)
            self.readEvent.clear()

    """
    Think About something.
    type: sentence, sensor, image
    """
    # 语句处理
    def thinkAboutSentence(self, sentence):
        # print("Bay max is sleeping: " + str(self.baymax.isSleeping()) + str(sentence))
        # 休眠状态下唤醒
        if self.baymax.isSleeping():
            isWakeup = wakeup.handle(self, sentence)
            if isinstance(isWakeup, str):
                return isWakeup
            else:
                return None

        # 句子意图处理
        intentionAnalyticsResult = UNIT.talk(sentence)
        if "result" in intentionAnalyticsResult:
            intentName = intentionAnalyticsResult["result"]["response_list"][0]["schema"]["intent"]

            if intentName in self.intentions:
                intentResult = self.intentions[intentName].handle(
                    self, sentence, intentionAnalyticsResult["result"]["response_list"]
                )

                if intentResult is True:
                    return None
                elif isinstance(intentResult, str):
                    return intentResult

        # 句子本地能力处理
        for ability in self.abilities:
            result = ability.handle(self, sentence)
            if result is True:
                return None
            elif isinstance(result, str):
                return result

        # 唱歌的时候 不接受闲聊的指令
        if Sound.isBusy() and Sound.isSong:
            return None

        result = Turing.ask(sentence)
        if not result["text"]:
            return None

        print("图灵说：" + result["text"])
        return result["text"]


    # 发送指令给器官
    def giveCommand(self, targetOrgan, command = None):
        if isinstance(targetOrgan, dict) and command is None and "targetOrgan" in targetOrgan:
            targetOrgan = targetOrgan["targetOrgan"]
            command = targetOrgan["command"]
        self.writeEvent.target = targetOrgan
        self.workQueues[targetOrgan].put(command)
        self.writeEvent.set()  # --> 发送写事件

    # 耳朵输入处理
    def inputWithEars(self, data):
        result = Baidu.voice2text(data["data"])
        sentence = None
        if 'result' in result.keys():
            sentence = result["result"][0][:-1]
            print("语音识别结果：" + sentence, result)

        if not sentence:
            return

        answer = self.thinkAboutSentence(sentence)
        if answer is not None:
            self.writeEvent.target = "Mouth"
            self.giveCommand("Mouth", {
                "type": "speak",
                "data": answer
            })

    # 皮肤输入处理
    def inputWithSkin(self, data):
        pass

    # 控制嘴巴输出
    def controlWithMouth(self, data):
        self.giveCommand(data["organ"], data["command"])
