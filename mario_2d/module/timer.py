class Timer(object):
    def __init__(self, t):
        self.startTime = t
        self.time = t
        self.startBool = False
        self.end = False

    def update(self):
        if self.startBool and self.time > 0 :
            self.time -= 1
        if self.time == 0 :
            self.startBool = False
            self.time = self.startTime

    def start(self):
        self.startBool = True
        self.update()

    def done(self):
        if self.time == 0 or self.time == self.startTime:
            return True
        else :
            return False