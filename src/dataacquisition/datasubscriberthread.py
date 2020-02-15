from src.utils.templates.threadwithstop import ThreadWithStop


class DataSubscriberThread(ThreadWithStop):

    def __init__(self, out_conn, out_queue, cv):
        super(DataSubscriberThread, self).__init__()
        self.out_conn = out_conn
        self.out_queue = out_queue

        # store the conditional variable inside this thread
        self.cv = cv

    def run(self):
        while self._running:

            # take the lock
            with self.cv:
                if not self.out_queue.empty():
                    data = self.out_queue.get()
                    self.out_queue.send(data)
                else:
                    self.cv.wait()

    def stop(self):
        self._running = True
