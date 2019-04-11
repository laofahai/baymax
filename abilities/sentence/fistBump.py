def handle(brain, sentence, intention = None):
    if "碰" in sentence and "拳" in sentence:
        brain.giveCommand("RightArm", {
            "type": "fistBump",
            "data": ""
        })
        return True
    return None
