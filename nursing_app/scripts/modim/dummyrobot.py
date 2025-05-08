import time, random

class DummyRobot:

    def _init_(self):
        pass

    def setAlive(self, v):
        pass

    def normalPosture(self):
        pass

    def setLanguage(self, v):
        pass

    def setVolume(self, v):
        pass

    def animation(self, interaction):
        pass

    def say(self, v):
        time.sleep(5)
        pass

    def asr(self, v, timeout=10):
        time.sleep(timeout)
        return None # random.choice(v)

    def asr_cancel(self):
        pass

    def showurl(self, weburl):
        print('show url: '+weburl)
        pass

    def stop(self):
        pass

    def startFaceDetection(self):
        pass

    def stopFaceDetection(self):
        pass

    def dance(self):
        print("Dummy Robot is dancing....")
    
    def sax(self):
        print("Dummy Robot is playing sax....")

def forward(v):
    pass

def backward(v):
    pass

def left(v):
    pass

def right(v):
    pass

