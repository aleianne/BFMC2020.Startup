from src.dataacquisition.imageprocessing.line import Line

from threading import Thread

import numpy as np
import logging

class LaneTracking:

    def __init__(self):
        self.lane = None

        self.bx = -1
        self.by = -1
        self.tx = -1
        self.ty = -1

        self.class_name = LaneTracking.__name__

        # displacement in pixel
        self.r_x = 5
        self.r_y = 5

        self.logger = logging.getLogger("bfmc.laneDetection.laneDetectionThread.laneTracking")

    # DEFINITION OF GET/SET METHODS

    def setLane(self, lane):
        self.lane = lane

    def getLane(self):
        return self.lane

    # DEFINITION OF PRIVATE METHODS

    def _removeNoise(self, img):
        pass

    def _detectMaximumIntensity(self, img, y_coord):
        img_row = img[y_coord, :]
        v = np.amax(img_row)
        index_x = np.where(v)
        return v, index_x

    def _searchLocalEndPoint2(self, img):
        size = img.shape[0]

        for y in range(0, size - 1):
            v, x = self._detectMaximumIntensity(img, y)
            if v > 200:
                return x, y

        return -1, -1

    def _searchLocalEndPoint(self, img):
        center_y = int(img.shape[0] / 2)
        upper_y = center_y - 1
        lower_y = center_y + 1

        v, x = self._detectMaximumIntensity(img, center_y)
        if v > 200:
            return x, center_y

        while upper_y > 0:
            v, x = self._detectMaximumIntensity(img, upper_y)
            if v > 200:
                return x, upper_y

            v, x = self._detectMaximumIntensity(img, lower_y)
            if v > 200:
                return x, lower_y

            upper_y -= 1
            lower_y += 1

        return -1, -1

    def _localInitialPointSearch(self, img):
        if (img.shape[0] >= (2 * self.r_y)) and (img.shape[1] >= (2 * self.r_x)):
            self.bx, self.by = self._searchLocalEndPoint(img)
        else:
            self.bx, self.by = self._searchLocalEndPoint2(img)

    def _localTerminalPointSearch(self, img):
        if (img.shape[0] >= (2 * self.r_x)) and (img.shape[1] >= (2 * self.r_x)):
            self.tx, self.ty = self._searchLocalEndPoint(img)
        else:
            self.tx, self.ty = self._searchLocalEndPoint2(img)

    def _detectRegionOfInterest(self, img, x, y):
        right_x_disp = x + self.r_x + 1
        left_x_disp = x - self.r_x

        right_y_disp = y + self.r_y + 1
        left_y_disp = y + self.r_y

        roi = img[left_y_disp:right_y_disp, left_x_disp:right_x_disp]
        return roi

    # DEFINITION OF PUBLIC METHODS

    def trackLane(self, img):

        if self.lane is None:
            self.logger.error("We cannot detect any lane")
            return False

        x1, y1 = self.lane.getInitialPoint()
        x2, y2 = self.lane.getTerminalPoint()

        # check if the initial point and the terminal point is contained inside the image
        if not(x1 <= img.shape[1] and y1 <= img.shape[0]):
            self.logger.error("The initial point of the segment exceed the image dimension...")
            return False

        if not(x2 <= img.shape[1] and y2 <= img.shape[0]):
            self.logger.error("The terminal point of the segment exceed the image dimension...")
            return False

        # detect the two different region of interest for the initial and the terminal point
        begin_point_roi = self._detectRegionOfInterest(img, x1, y1)
        term_point_roi = self._detectRegionOfInterest(img, x2, y2)

        # search the maximum value of intensity into the two different region of interest
        # using two different threads

        thread1 = Thread(target=self._localInitialPointSearch, args=(begin_point_roi,))
        thread2 = Thread(target=self._localTerminalPointSearch, args=(term_point_roi,))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        if self.bx >= 0 and self.tx >= 0:
            self.logger.debug("Lane features updated correctly")
            self.lane = Line(self.bx, self.by, self.tx, self.ty)
            return True
        else:
            self.logger.debug("Impossible to update lane features")
            return False