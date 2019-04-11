from utils.sound import Sound
from utils.client.baidu import Baidu
import time
import pygame

def handle(brain, sentence, responseList):

    if Sound.isBusy() and not Sound.isSong:
        return None

    if "上" in sentence:
        Sound.stop()
        time.sleep(.5)
        brain.giveCommand("Mouth", {
            "type": "singPrevious"
        })
    elif "下" in sentence:
        Sound.stop()
        time.sleep(.5)
        brain.giveCommand("Mouth", {
            "type": "singNext"
        })
    elif "暂停" in sentence:
        Sound.stop()
    elif "继续" in sentence:
        Sound.unpause()
    elif "停" in sentence or "闭嘴" in sentence or "晚安" in sentence or "不想" in sentence:
        Sound.stop()
    elif "重新" in sentence:
        Sound.stop()
        time.sleep(.5)
        brain.giveCommand("Mouth", {
            "type": "replayCurrent"
        })
    elif "快" in sentence:
        Baidu.speed += 1
    elif "慢" in sentence:
        Baidu.speed -= 1
    elif "大" in sentence:
        pygame.mixer.music.set_volume(
            pygame.mixer.music.get_volume() + .1
        )
    elif "小" in sentence:
        pygame.mixer.music.set_volume(
            pygame.mixer.music.get_volume() - .1
        )
    else:
        return None

    return True

