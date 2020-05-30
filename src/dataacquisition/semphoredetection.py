from src.utils.templates.threadwithstop import ThreadWithStop
from src.dataacquisition.imageprocessing.imagesegmentation import ImageSegmentation
from src.dataacquisition.imageclassification.semaphoredetection import SemaphoreDetection
from src.utils.debugger.videologger import VideoLogger

import logging


class SemaphoreDetectionThread(ThreadWithStop):

    def __init__(self, in_conn, out_queue, cv, video_debug=False):
        super(SemphoDetectionThread, self).__init__()
        self.in_conn = in_conn
        self.out_queue = out_queue

        self.cv = cv

        self.logger = logging.getLogger("bfmc.objectDetection.semaphoreDetectionThread")

        if video_debug:
            self.video_logger = VideoLogger()

        self.image_segmentation = ImageSegmentation()
        self.dnn = semphoredetection()


        self.semphore_detected = False          #?if modification is needed?

        self.last_ts = None                 # last frame timestamp
        self.last_dts = None                # last frame with traffic sign detected

    def _writesemaphoreDetected(self, det_ts):
        with self.cv:
            for ts in det_ts:
                self.out_queue.put(ts)
            self.cv.notify()

    def run(self):

        self.logger.info("Started semaphore detection")

        while self._running:
            try:
                # retrieve the image and the timestamp from the input connection
                data = self.in_conn.recv()
                timestamp = data[0][0]
                image = data[1]

                self.image_segmentation.detectObjectOfInterest(image)

                if self.image_segmentation.getObjectDetected():
                    self.last_dts = timestamp
                    self.semphore_detected = True
                    detected_object_list = self.image_segmentation.getObjectDetected()
                    self._writesemaphoreDetected()Detected(detected_object_list)

                    object_n = len(detected_object_list)
                    self.logger.debug("Detected {n} object!".format(n=object_n))
                else:
                    self.logger.debug("No object has been detected")
                    self.semaphore_detected = False

                self.last_ts = timestamp

            except EOFError:
                self.logger.error("Input connection has been closed")
                self._running = False

    def stop(self):
        self.logger.debug("Forced the interruption of the computation")
        self._running = False
