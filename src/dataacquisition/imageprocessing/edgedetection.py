from src.dataacquisition.imageprocessing.line import Line

import cv2
import math
import numpy as np


class EdgeDetection:

    def __init__(self):
        self.right_lanes = []
        self.left_lanes = []

        self.lane_detected = False

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

    # DEFINITION OF PRIVATE METHODS

    def _detectLineSegments(self, cropped_img):
        # GENERATING THE LINES USING HOUGH TRANSFORM
        # rho is the distance precision in pixel.
        # angle is angular precision in radian.
        # min_threshold is the number of votes needed to be considered a line segment
        # minLineLength is the minimum length of the line segment in pixels.
        # maxLineGap is the maximum in pixels that two line segments that can be separated and still be considered a single line segment.
        # CHANGE THE rho, theta, threshold, minLineLength, and maxLineGap
        line_segments = cv2.HoughLinesP(cropped_img,
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
        # The number of color channels
        # channel_count = img.shape[2]
        match_mask_color = 255
        cv2.fillPoly(mask, vertices, match_mask_color)
        masked_image = cv2.bitwise_and(img, mask)
        return masked_image

    def _cannyEdge(self, img):
        return cv2.Canny(img, 100, 200)

    # DEFINITION OF PUBLIC METHODS

    def laneDetection(self, image):
        region_of_interest_vertices = [
            (0, image.shape[0]),
            (image.shape[1] / 2, image.shape[0] / 2),
            (image.shape[1], image.shape[0]),
        ]

        # convert the image in grays cale and than extract the region of interest
        canny_image = self._cannyEdge(image)
        cropped_image = self._regionOfInterest(
            canny_image,
            np.array([region_of_interest_vertices], np.int32),
        )

        # generate the lines using the hough transform
        line_segments = self._detectLineSegments(cropped_image)

        left_lane_x = []
        left_lane_y = []

        right_lane_x = []
        right_lane_y = []

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

        if (len(left_lane_x) == 0) and (len(right_lane_x) == 0):
            self.lane_detected = False
            return

        if len(left_lane_x) != 0:
            poly_left = np.poly1d(np.polyfit(
                left_lane_y,
                left_lane_x,
                deg=1
            ))

            left_x_start = int(poly_left(max_y))
            left_x_end = int(poly_left(min_y))

            left_lane = Line(left_x_start, min_y, left_x_end, max_y)
            self.left_lanes.append(left_lane)

        if len(right_lane_x) != 0:
            poly_right = np.poly1d(np.polyfit(
                right_lane_y,
                right_lane_x,
                deg=1
            ))

            right_x_start = int(poly_right(max_y))
            right_x_end = int(poly_right(min_y))

            right_lane = Line(right_x_start, min_y, right_x_end, max_y)
            self.right_lanes.append(right_lane)

        self.lane_detected = True
        return self.lane_detected
