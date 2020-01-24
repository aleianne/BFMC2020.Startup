from src.utils.templates.threadwithstop import ThreadWithStop

class CameraAcquirer(ThreadWithStop):

    def __init__(self, inConn):
    	super(CameraAcquirer, self).__init__()
        self.inConn = inConn

    def run(self):

        while self._running:
            try: 
                # iterate over all the possible pipe incoming into the process
                data_read = inConn.recv()
                time = data_read[0][0]
                image = data_read[1]
                # print("Image timestamp " + str(time))
                # this function should return the information about the lane detected on the floor
                # lane_detector(image)  
            except EOFError:
                print("CameraAcquirer: the incoming connection has been closed")
                self._running = False

    def stop():
        self._running = False