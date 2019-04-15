def handle(brain, sentence, intention = None):
    if "摇头" in sentence:

        brain.giveCommand("Head", {
            "type": "shake",
            "data": ""
        })
        return True

    return None
