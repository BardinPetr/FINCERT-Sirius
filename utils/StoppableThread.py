import threading


class StoppableThread(threading.Thread):
    def __init__(self, x):
        super(StoppableThread, self).__init__(target=x)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
