
def handle(brain, sentence, intention = None):
    if "不" not in sentence and ("服务" in sentence and "满意" in sentence):
        brain.baymax.organs["Mouth"].speak("谢谢，我将进入休眠，再见")

        brain.giveCommand("LeftArm", {
            "type": "wave",
            "data": ""
        })
        brain.baymax.sleep()
        return True
    return None
