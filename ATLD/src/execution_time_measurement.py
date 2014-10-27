__author__ = 'Francesco'

import time


class ExecutionTimeMeasurement:

    start = 0
    finish = 0
    interval = 0

    def __init__(self):
        pass

    def start_measurement(self):
        self.start = time.clock()

    def finish_measurement(self):
        self.finish = time.clock()
        self.interval = (self.start - self.finish)

    def get_measurement_interval(self):
        return abs(self.interval)


