from src.utils.templates.threadwithstop import ThreadWithStop
from src.dataacquisition.imageprocessing.imagesegmentation import ImageSegmentation
from src.dataacquisition.imageclassification.signclassification import SignClassification
from src.utils.debugger.videologger import VideoLogger

import logging


class SignDetectionThread(ThreadWithStop):

    def __init__(self, in_conn, out_queue, cv, video_debug=False):
        super(SignDetectionThread, self).__init__()
        self.in_conn = in_conn
        #self.out_queue = out_queue

        #self.cv = cv

        self.logger = logging.getLogger("bfmc.objectDetection.signDetectionThread")

        if video_debug:
            self.video_logger = VideoLogger()

        self.image_segmentation = ImageSegmentation()
        self.dnn = SignClassification()


        self.sign_detected = False

        self.last_ts = None                 # last frame timestamp
        self.last_dts = None                # last frame with traffic sign detected

    def _writeTrafficSignDetected(self, det_ts):
        pass
    #    with self.cv:
     #       for ts in det_ts:
      #          self.out_queue.put(ts)
       #     self.cv.notify()

    def run(self):

        self.logger.info("Started traffic sign detection")

        while self._running:
            print("here is before try")  #测试
            try:
                # retrieve the image and the timestamp from the input connection
                data = self.in_conn.recv()
                timestamp = data[0][0]
                image = data[1]

                self.image_segmentation.detectObjectOfInterest(image)
                print("I AM HERE 01")   #测试
                if self.image_segmentation.getObjectDetected():
                    self.last_dts = timestamp
                    self.sign_detected = True
                    detected_object_list = self.image_segmentation.getObjectDetected()
                    self._writeTrafficSignDetected(detected_object_list)

                    object_n = len(detected_object_list)
                    self.logger.debug("Detected {n} object!".format(n=object_n))
                else:
                    self.logger.debug("No object has been detected")
                    self.sign_detected = False

                self.last_ts = timestamp

            except EOFError: 
                self.logger.error("Input connection has been closed")
                self._running = False

            except Exception:
                print("here is  an exception")

    def stop(self):
        self.logger.debug("Forced the interruption of the computation")
        self._running = False
