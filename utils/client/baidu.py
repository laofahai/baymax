from aip import AipSpeech
from utils.configure import Configure

class Baidu:

    client = None

    voicePath = "data/audio/machine.mp3"

    devPid = 1537

    speed = 4
    per = 1
    pit = 0
    vol = 10

    @staticmethod
    def init():
        if Baidu.client is None:
            Baidu.client = AipSpeech(
                Configure.get("baiduSpeach", "APP_ID"),
                Configure.get("baiduSpeach", "API_KEY"),
                Configure.get("baiduSpeach", "SECRET_KEY")
            )

    @staticmethod
    def voice2text(voicePath):
        Baidu.init()
        with open(voicePath, 'rb') as fp:
            fileContent = fp.read()

        result = Baidu.client.asr(fileContent, 'wav', 16000, {'dev_pid': Baidu.devPid,})

        return result

    @staticmethod
    def text2voice(words, fileName = None):
        Baidu.init()
        result = Baidu.client.synthesis(words, 'zh', 1, {
            'vol':Baidu.vol,
            'spd':Baidu.speed,
            'per':Baidu.per,
            'pit':Baidu.pit
        })

        if fileName:
            path = "data/audio/" + fileName + ".mp3"
        else:
            path = Baidu.voicePath

        if not isinstance(result, dict):  
            with open(path, 'wb') as f:
                f.write(result)

        return path
