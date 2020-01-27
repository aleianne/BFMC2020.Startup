class LaneTracking():

    def __init__(self):
        self.endpoint_x = []
        self.endpoint_y = []

        # definition of the range maxmimum value in pixel
        self.range_px = 10

    # DEFIION OF GET/SET METHODS

    def getEndPointX(self):
        return self.endpoint_x

    def getEndPointY(self):
        return self.endpoint_y

    # DEFINITION OF PUBLIC METHODS

    def beginToTrack(self, image):
        pass
