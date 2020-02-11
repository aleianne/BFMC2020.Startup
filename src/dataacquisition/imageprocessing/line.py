class Line:

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2

        self.y1 = y1
        self.y2 = y2

        num = self.y1 - self.y2
        den = self.x1 - self.x2
        self.slope = num / den

    # DEFINITION OF GET/SET METHODS

    def getSlope(self):
        return self.slope

    def getPointx1(self):
        return self.x1

    def getPointx2(self):
        return self.x2

    def getPointy1(self):
        return self.y1

    def getPointy2(self):
        return self.y2

    # DEFINITION OF PUBLIC METHODS

    def getInitialPoint(self):
        if self.y1 <= self.y2:
            return self.x1, self.y1
        else:
            return self.x2, self.y2

    def getTerminalPoint(self):
        if self.y1 >= self.y2:
            return self.x1, self.y1
        else:
            return self.x2, self.y2



