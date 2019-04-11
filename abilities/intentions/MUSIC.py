from utils.client.unit import UNIT
import re


def handle(brain, sentence, responseList):

    slots = UNIT.parseSlot(responseList[0]["schema"]["slots"])

    playSource = "kugou"

    if "故事" in sentence:
        playSource = "ximalaya"

    # 没有解析到词槽
    if len(slots) > 0:
        keyword = []

        if "user_music_artist" in slots:
            keyword.append(slots["user_music_artist"]["normalized_word"])
        if "user_music_name" in slots:
            keyword.append(slots["user_music_name"]["normalized_word"])

        brain.giveCommand("Mouth", {
            "type": "sing",
            "data": {
                "keyword": " ".join(keyword),
                "source": playSource
            }
        })
    else:
        keyword = re.sub("[我要听|我想听|想听|要听|的歌]", "", sentence)

        brain.giveCommand("Mouth", {
            "type": "sing",
            "data": {
                "keyword": keyword,
                "source": playSource
            }
        })


    return True
