from src.dataacquisition.imageprocessing.line import Line

from threading import Thread

class LaneTracking:

    def __init__(self):
        self.lane = None

        self.bx = -1
        self.by = -1
        self.tx = -1
        self.ty = -1

        # maximum range in pixel
        self.range_x = 10
        self.range_y = 10

    # DEFINITION OF GET/SET METHODS
    def setLane(self, lane):
        self.lane = lane

    def getLane(self):
        return self.lane

    # DEFINITION OF PRIVATE METHODS

    def _removeNoise(self, img):
        # this method should perform some kind of noise reduction
        # detecting and removing outliers
        pass

    def _localBeginPointSearch(self, img):

        pass

    def _localTerminalPointSearch(self, img):
        pass

    # this method is called inside a thread, in this way we can split our computation since
    # the local search is performed in two different areas. Starting from the point passed to the function
    # try to extract a ROI of 10 px starting from the end-point
    def _localSearchDetection(self, img):
        pass

    def _detectRegionOfInterest(self, img, x, y):
        # crop the image in order to detect the local search area
        # centered around the point (x, y)
        x_v = int(self.range_x / 2)
        y_v = int(self.range_y / 2)
        roi = img[x - x_v:x + x_v, y - y_v:y + y_v]
        return roi

    # DEFINITION OF PUBLIC METHODS

    def trackLane(self, img):

        if self.lane is None:
            return

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
            # create a new lane
            self.lane = Line(self.bx, self.by, self.tx, self.ty)
            return True
        else:
            print('Impossible to detect a new line')
            return False

