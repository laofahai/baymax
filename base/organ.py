import threading

class OrganBase(threading.Thread):

    def __init__(self, brainWorkQueue, selfWorkQueue, writeEvent, readEvent):
        super().__init__()
        self.brainWorkQueue = brainWorkQueue
        self.selfWorkQueue = selfWorkQueue
        self.writeEvent = writeEvent
        self.readEvent = readEvent
        self.name = "Ears"
        self.daemon = True

    def notifyBrain(self, data):

        self.readEvent.target = self.getName()

        self.brainWorkQueue.put(data)
        self.readEvent.set()
