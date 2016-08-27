import time

class Timer(object):
    def __init__(self):
        self.timers = {}

    def start(self, event):
        self.timers[event] = time.time()

    def end(self, event):
        total_time = time.time() - self.timers[event]
        self.timers[event] = total_time
        return total_time

    def print_times(self):
        for event in self.timers:
            print "Time for {}: {} seconds".format(event, self.timers[event])
