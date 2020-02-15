from src.dataacquisition.imageprocessing.line import Line

import logging
import cv2 as cv
import math
import numpy as np


class EdgeDetection:

    def __init__(self):
        self.right_lanes = []
        self.left_lanes = []

        self.lane_detected = False

        self.last_dts = None                # timestamp of the last lane detected inside a frame

    # DEFINITION OF GET/SET METHODS

    def getLastDetectedRLane(self):
        if len(self.right_lanes) != 0:
            return self.right_lanes[-1]
        else:
            return None

    def getLastDetectedLLane(self):
        if len(self.left_lanes) != 0:
            return self.left_lanes[-1]
        else:
            return None

    def getRightLanes(self):
        return self.right_lanes

    def getLeftLanes(self):
        return self.left_lanes

    def getLaneDetected(self):
        return self.lane_detected

    def initDetection(self):
        self.right_lanes = []
        self.left_lanes = []

        self.lane_detected = False

    # DEFINITION OF PRIVATE METHODS

    def _detectLineSegments(self, cropped_img):
        line_segments = cv.HoughLinesP(cropped_img,
                                        rho=6,
                                        theta=np.pi / 60,
                                        threshold=160,
                                        lines=np.array([]),
                                        minLineLength=40,
                                        maxLineGap=25
                                        )

        return line_segments

    def _regionOfInterest(self, img, vertices):
        mask = np.zeros_like(img)
        match_mask_color = 255
        cv.fillPoly(mask, vertices, match_mask_color)
        masked_image = cv.bitwise_and(img, mask)
        return masked_image

    def _fitLane(self, lane_x, lane_y, max_y, min_y):
        poly_left = np.poly1d(np.polyfit(
            lane_y,
            lane_x,
            deg=1
        ))

        x_start = int(poly_left(max_y))
        x_end = int(poly_left(min_y))

        new_line = Line(x_start, min_y, x_end, max_y)
        return new_line

    # DEFINITION OF PUBLIC METHODS

    def laneDetection(self, image, ts):


        # TODO da controllare se questa regione di interesse è corretta o meno
        # in particolare non saprei se questo triangolo è la cosa migliore da passare
        # define the region of interest
        region_of_interest_vertices = [
            (0, image.shape[0]),
            (image.shape[1] / 2, image.shape[0] / 2),
            (image.shape[1], image.shape[0]),
        ]

        # convert the image in grays cale and than extract the region of interest
        canny_image = cv.Canny(image, 100, 200)
        cropped_image = self._regionOfInterest(
            canny_image,
            np.array([region_of_interest_vertices], np.int32),
        )

        # generate lines using the hough transform
        line_segments = self._detectLineSegments(cropped_image)

        if len(line_segments) == 0:
            return False

        left_lane_x = []
        left_lane_y = []

        right_lane_x = []
        right_lane_y = []

        # this part of the code detect only right and left lane marker
        for line in line_segments:
            for x1, y1, x2, y2 in line:
                slope = (y2 - y1) / (x2 - x1)

                if math.fabs(slope) < 0.5:
                    continue

                if slope <= 0:
                    left_lane_x.extend([x1, x2])
                    left_lane_y.extend([y1, y2])
                else:
                    right_lane_x.extend([x1, x2])
                    right_lane_y.extend([y1, y2])

        min_y = int(image.shape[0] * (3 / 5))
        max_y = image.shape[0]

        if (len(left_lane_x) == 0) or (len(right_lane_x) == 0):
            self.lane_detected = False
            return False

        self.left_lanes.append(self._fitLane(left_lane_x, left_lane_y, max_y, min_y))
        self.right_lanes.append(self._fitLane(right_lane_x, right_lane_y, max_y, min_y))
        self.lane_detected = True
        self.last_dts = ts

        return True

        # poly_left = np.poly1d(np.polyfit(
        #     left_lane_y,
        #     left_lane_x,
        #     deg=1
        # ))
        #
        # left_x_start = int(poly_left(max_y))
        # left_x_end = int(poly_left(min_y))
        #
        # left_lane = Line(left_x_start, min_y, left_x_end, max_y)
        # self.left_lanes.append(left_lane)

        # if len(right_lane_x) != 0:
        #     poly_right = np.poly1d(np.polyfit(
        #         right_lane_y,
        #         right_lane_x,
        #         deg=1
        #     ))
        #
        #     right_x_start = int(poly_right(max_y))
        #     right_x_end = int(poly_right(min_y))
        #
        #     right_lane = Line(right_x_start, min_y, right_x_end, max_y)
        #     self.right_lanes.append(right_lane)
