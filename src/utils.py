import time


class TimeOracle:
    def __init__(self):
        self.initial_perf_time = time.time() - time.perf_counter()

    def get_current_time(self):
        return self.initial_perf_time + time.perf_counter()
    
    @staticmethod
    def get_readable_time(current_time):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time))
