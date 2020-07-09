from src.utils.templates.threadwithstop import ThreadWithStop
from src.utils.debugger.initlogger import InitLogger

import logging
import cv2
import numpy as np


class SignDetectionThread(ThreadWithStop):

    def __init__(self, in_conn):
        super(SignDetectionThread, self).__init__()
        self.in_conn = in_conn
        self.logger = logging.getLogger("bfmc.objectDetection.signDetectionThread")

        initLogger = InitLogger()
        self.debug_directory = initLogger.getDebugDir()

    def run(self):
        self.logger.info("Started traffic sign detection")

        while self._running:
            try:
                # retrieve the image and the timestamp from the input connection
                data = self.in_conn.recv()
                timestamp = data[0][0]
                image = data[1]
                self._performDetection(image, timestamp)
            except EOFError:
                self.logger.error("Input connection has been closed")
                self._running = False

    def stop(self):
        self.logger.debug("Forced the interruption of the computation")
        self._running = False

    def _saveImages(self, images, timestamp):
        i = 0
        for image in images:
            if len(image) != 0:
                image_name = str(timestamp) + '_' + str(i) + '.jpg'
                i += 1
                path = self.debug_directory / image_name
                cv2.imwrite(str(path), image)

    def _performDetection(self, image, timestamp):
        images = []

        # convert colors
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        blue_lower = np.array([100, 50, 50])
        blue_upper = np.array([124, 255, 255])

        # mask
        mask = cv2.inRange(hsv, blue_lower, blue_upper)
        blurred = cv2.blur(mask, (9, 9))
        images.append(blurred)

        # binarization
        ret, binary = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
        images.append(binary)

        # closed
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
        closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        # erode and dilate
        erode = cv2.erode(closed, None, iterations=4)
        dilate = cv2.dilate(erode, None, iterations=4)

        contours, hierarchy = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        res = image.copy()

        for con in contours:
            rect = cv2.minAreaRect(con)
            # box
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            # the segmentation area on original image
            cv2.drawContours(res, [box], -1, (0, 0, 255), 2)
            #print([box])
            # the dimension of matrix
            h1 = min(box.max(axis=0))
            h2 = min(box.min(axis=0))
            l1 = max(box.max(axis=1))
            l2 = min(box.max(axis=1))

            # make sure if the area is accurate
            if h1 - h2 > 0 and l1 - l2 > 0:
                # segmentation
                temp = image[h2:h1, l2:l1]
                images.append(temp)

        self._saveImages(images, timestamp)