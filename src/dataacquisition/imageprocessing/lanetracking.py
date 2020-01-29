class LaneTracking:

    def __init__(self):
        self.lane = None

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

    # DEFINITION OF PUBLIC METHODS

    def trackLane(self, img):

        if self.lane is None:
            return

        x1 = self.lane.getPointx1()
        x2 = self.lane.getPointx2()

        y1 = self.lane.getPointy1()
        y2 = self.lane.getPointy2()

        # matching with the edge detected in the original frame


