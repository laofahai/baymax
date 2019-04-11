wakeUpWords = [
    '大白','大呗','你好大呗','你好大白',
    '你好的呗','大呗你好','打败你好','大白你好',
    '你好大牌', '好的白', '好的呗', '好打败',
    '好大呗', '好大白', '挺好的呗'
]

def handle(brain, sentence, intention = None):
    if sentence in wakeUpWords:
        brain.baymax.wakeup()
        return True

    return None
