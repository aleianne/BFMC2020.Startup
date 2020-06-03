from src.utils.templates.threadwithstop import ThreadWithStop
from src.dataacquisition.imageprocessing.semaphoredetection import SemaphoreDetection

from src.utils.debugger.videologger import VideoLogger

import logging
import cv2
import random
import numpy as np
from enum import Enum
import matplotlib.pyplot as plt
import matplotlib.image as mpimg



class SemaphoreDetectionThread(ThreadWithStop):

    def __init__(self, in_conn, video_debug=False):
        super(SemaphoreDetectionThread, self).__init__()
        self.in_conn = in_conn

        self.logger = logging.getLogger("bfmc.objectDetection.semaphoreDetectionThread")

        self.video_logger = VideoLogger()
        self.detect_semaphore = SemaphoreDetection()

        self.semaphore_detected = False

        self.last_ts = None
        self.last_dts = None

    def run(self):
        self.logger.info("Started semaphore detection")

        while self._running:
            print(" before try")
            try:
                data = self.in_conn.recv()
                timestamp = data[0][0]
                image = data[1]
                overallState = self.detect_semaphore.detectState(image)
                print("The state returned by the detectState function is {state}".format(state=overallState))

                if self.detect_semaphore.getObjectDetected():
                    self.last_dts = timestamp
                    self.semaphore_detected = True
                    detected_object_list = self.detect_semaphore.getObjectDetected()
                    # self._writeTrafficSignDetected(detected_object_list)

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
