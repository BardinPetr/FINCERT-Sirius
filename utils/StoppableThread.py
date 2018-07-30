import threading
import time


class StoppableThread(threading.Thread):
    @staticmethod
    def wait(t, trg):
        time.sleep(t)
        trg()

    def __init__(self, x, start_timeout=0):
        trg = lambda: StoppableThread.wait(start_timeout, x) if start_timeout != 0 else x
        super(StoppableThread, self).__init__(target=trg)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
