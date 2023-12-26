import time


class TimeOracle:
    def __init__(self):
        self.initial_perf_time = time.time() - time.perf_counter()
        self.model = None

    def get_current_time(self):
        return self.initial_perf_time + time.perf_counter()

    @staticmethod
    def get_readable_time(current_time):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time))

    def set_model(self, model):
        self.model = model

    def update_model(self):
        if not self.model:
            raise RuntimeError

        while True:
            time.sleep(60)
            try:
                self.model.update_data()
            except RuntimeError:
                break
