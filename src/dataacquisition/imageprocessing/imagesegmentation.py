import cv2 as cv2
import numpy as np

import logging

class ImageSegmentation:

    def __init__(self):
        # define the lower and upper bound for the red and blue value
        self.blue_lower = np.array([100, 50, 50])
        self.blue_upper = np.array([124, 255, 255])

        self.BoI = []

        self.object_detected = False

        self.logger = logging.getLogger("bfmc.objectDetection.signDetectionThread.imageSegmentation")

    def getObjectDetected(self):
        if len(self.BoI) > 0:
            return True
        else:
            return False

    def getBlobOfInterst(self):
        return self.BoI

    def _checkContours(self, contours):
        if len(contours) < 1:
            self.logger.debug("Impossible to detect contours inside the frame")
            return False

    def _checkSingleContour(self, contour):
        if len(contour) < 1:
            self.logger.debug("Contour is empty...")
            return False
        else:
            for point in contour:
                x = point[0]
                y = point[1]

                if x > 0 and y > 0:
                    return True

            return False


    def initSegmentation(self):
        # delete the list of BoI
        self.BoI = []

    def detectObjectOfInterest(self, img):
        self.initSegmentation()

        # convert the image in HSV representation
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        # mask
        mask = cv.inRange(hsv, self.blue_lower, self.blue_upper)

        # reducing noise
        # blur
        blurred = cv.blur(mask, (9, 9))

        # binarization
        ret, binary = cv.threshold(blurred, 127, 255, cv.THRESH_BINARY)

        # closed
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (21, 7))
        closed = cv.morphologyEx(binary, cv.MORPH_CLOSE, kernel)

        # erode and dilate
        erode = cv.erode(closed, None, iterations=4)
        dilate = cv.dilate(erode, None, iterations=4)

        contours, hir = cv.findContours(dilate.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        res = img.copy()

        for con in contours:

            if self._checkSingleContour(con):

                rect = cv.minAreaRect(con)

                # box
                box = cv.boxPoints(rect)
                box = np.int0(box)
                # the segmentation area on original image
                cv.drawContours(res, [box], -1, (0, 0, 255), 2)
                print([box])
                # the dimension of matrix
                h1 = min(box.max(axis=0))
                h2 = min(box.min(axis=0))
                l1 = max(box.max(axis=1))
                l2 = min(box.max(axis=1))
                print('h1', h1)
                print('h2', h2)
                print('l1', l1)
                print('l2', l2)
                # make sure if the area is accurate
                if h1 - h2 > 0 and l1 - l2 > 0:
                    # segmentation
                    temp = img[h2:h1, l2:l1]

                    # turn it into 40*40
                    atemp = cv.resize(temp, (40, 40), interpolation=cv.INTER_CUBIC)

                    self.BoI.append(atemp)

