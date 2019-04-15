def handle(brain, sentence, intention = None):
    if "碰" in sentence and "拳" in sentence:
        brain.giveCommand("RightArm", {
            "type": "fistBump",
            "data": ""
        })
        return True
    elif "握" in sentence and "手" in sentence:
        brain.giveCommand("RightArm", {
            "type": "shakeHand",
            "data": ""
        })
        return True
    elif "再见" in sentence or "拜拜" in sentence:
        brain.giveCommand("LeftArm", {
            "type": "wave",
            "data": ""
        })
        brain.baymax.organs["Mouth"].speak("再~见~~~~")
        return True
    return None
