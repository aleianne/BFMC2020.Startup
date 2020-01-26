from src.utils.templates.threadwithstop import ThreadWithStop
from src.dataacquisition.imageprocessing.edgedetection import EdgeDetection

class CameraAcquirer(ThreadWithStop):

    def __init__(self, inConn):
    	super(CameraAcquirer, self).__init__()
      self.inConn = inConn

      self.edge_detection = EdgeDetection()

    def run(self):

        while self._running:
            try: 
                # iterate over all the possible pipe incoming into the process
                data_read = inConn.recv()
                time = data_read[0][0]
                image = data_read[1]

                if not self.edge_detection.getLaneDetected:
                  self.edge_detection.laneDetection(image)
                else: 
                  # track the image 
                  pass

            except EOFError:
                print("CameraAcquirer: the incoming connection has been closed")
                self._running = False

    def stop():
        self._running = False