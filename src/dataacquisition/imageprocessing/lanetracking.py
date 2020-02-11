from src.dataacquisition.imageprocessing.line import Line

from threading import Thread

import numpy as np


class LaneTracking:

    def __init__(self, cam_debugger, debug=False):
        self.lane = None

        self.bx = -1
        self.by = -1
        self.tx = -1
        self.ty = -1

        self.cam_debugger = cam_debugger
        self.debug = debug
        self.class_name = LaneTracking.__name__

        # displacement in pixel
        self.r_x = 5
        self.r_y = 5

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

    def _localBeginPointSearch(self, img):
        if img.size[0] >= 2 * self.r_y and img.size[1] >= 2 * self.r_x:
            self.bx, self.by = self._searchLocalEndPoint(img)
        else:
            self.bx, self.by = self._searchLocalEndPoint2(img)

    def _localTerminalPointSearch(self, img):
        if img.size[0] >= 2 * self.r_x and img.size[1] >= 2 * self.r_x:
            self.tx, self.ty = self._searchLocalEndPoint(img)
        else:
            self.tx, self.ty = self._searchLocalEndPoint2(img)

    def _detectRegionOfInterest(self, img, x, y):
        right_x_disp = x + self.r_x + 1
        left_x_disp = x - self.r_x

        right_y_disp = y + self.r_y + 1
        left_y_disp = y + self.r_y

        roi = img[left_x_disp:right_x_disp, left_y_disp:right_y_disp]
        return roi

    # DEFINITION OF PUBLIC METHODS

    def trackLane(self, img):

        if self.lane is None:
            return False

        x1, y1 = self.lane.getInitialPoint()
        x2, y2 = self.lane.getTerminalPoint()

        # detect the two different region of interest
        begin_point_roi = self._detectRegionOfInterest(img, x1, y1)
        term_point_roi = self._detectRegionOfInterest(img, x2, y2)

        # search the maximum value of intensity into the two different region of interest
        # using two different threads

        thread1 = Thread(target=self._localBeginPointSearch, args=(begin_point_roi,))
        thread2 = Thread(target=self._localTerminalPointSearch, args=(term_point_roi,))

        thread1.join()
        thread2.join()

        if self.bx >= 0 and self.tx >= 0:
            # update the lane detected
            self.lane = Line(self.bx, self.by, self.tx, self.ty)
            return True
        else:
            if self.debug:
                self.cam_debugger.write(self.class_name, "Impossible to track lanes")
            return False
