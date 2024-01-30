from threading import Thread, Event

class ResettableTimer(Thread):
    def __init__(self, interval, function, args=[], kwargs={}):
        super().__init__()
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = Event()
        self.resetted = True

    def cancel(self):
        self.finished.set()

    def run(self):
        while self.resetted:
            self.resetted = False
            self.finished.wait(self.interval)
            if not self.finished.isSet():
                self.function(*self.args, **self.kwargs)
                self.finished.set()

    def reset(self, interval=None):
        if interval:
            self.interval = interval
        self.resetted = True
        self.finished.set()
        self.finished.clear()
