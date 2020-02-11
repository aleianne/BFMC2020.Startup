from src.utils.templates.threadwithstop import ThreadWithStop
from src.dataacquisition.imageprocessing.imagesegmentation import ImageSegmentation
from src.dataacquisition.imageclassification.signclassification import SignClassification


class SignDetectionThread(ThreadWithStop):

    def __init__(self, in_conn):
        super(SignDetectionThread, self).__init__()
        self.in_conn = in_conn

        self.seg = ImageSegmentation()
        self.dnn = SignClassification()

        self.sign_detected = False

        self.last_ts = None                 # last frame timestamp
        self.last_dts = None                # last frame with traffic sign detected

    def run(self):

        while self._running:
            try:
                # retrieve the image and the timestamp from the input connection
                data = self.in_conn.recv()
                timestamp = data[0][0]
                image = data[1]

                self.seg.detectObjectOfInterest(image)

                if self.seg.getObjectDetected():
                    self.last_dts = timestamp
                    self.sign_detected = True

                    detected_object_list = self.seg.getObjectDetected()
                else:
                    print("No object has been detected inside our frame")
                    self.sign_detected = False

                self.last_ts = timestamp

            except EOFError: 
                print("SignDetectionThread: input connection has been closed")
                self._running = False

    def stop(self):
        self._running = False