from src.utils.templates.threadwithstop import ThreadWithStop

class SignDetectionThread(ThreadWithStop):

    def __init__(inPs):
        super(SignDetectionThread, self).__init__()
        self.inPs = inPs

    def run():

        if len(self.inPs) == 0:
            print("SingDetectionThread: no input connection has been specified")
            return
        elif len(self.inPs) != 1:
            print("SignDetectionThread: too many input connection, " + len(self.inPs))
            return

        inConn = self.inPs[0]

        while self._running:
            try:
                # retrieve the image and the timestamp from the input connection
                data = inConn.recv()
                timestamp = data[0][0]
                image = data[1]
            except EOFError: 
                print("SignDetectionThread: input connection has been closed")
                self._running = False

    def stop():
        self._running = False

     
