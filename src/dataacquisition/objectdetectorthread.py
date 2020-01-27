from src.utils.templates.threadwithstop import ThreadWithStop

class ObjectDetectorThread(ThreadWithStop):

    def __init__(self, inConn):
        super(ObjectDetectorThread, self).__init__()
        self.inConn = inConn                            # input pipe connection

    def run(self):
        while self._running == True:
            try: 
                data_in = self._inConn.recv()
                timestamp = data_in[0][0]
                image = data_in[1]
            except EOFError: 
                print("ObjectDetectorThread: input connection has been closed")
                self._running = False
        
    def stop(self):
        self._running = False