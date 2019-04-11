def handle(brain, sentence, responseList):

    playSource = "ximalaya"

    brain.giveCommand("Mouth", {
            "type": "sing",
            "data": {
                "keyword": "",
                "source": playSource
            }
        })

    return True
