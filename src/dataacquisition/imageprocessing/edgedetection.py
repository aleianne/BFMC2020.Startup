from src.dataacquisition.imageprocessing.line import Line

import logging
import cv2 as cv2
import math
import numpy as np

import logging

class EdgeDetection:

    def __init__(self):
        self.right_lanes = []
        self.left_lanes = []

        self.lane_detected = False

        self.last_dts = None                # timestamp of the last lane detected inside a frame
        self.logger = logging.getLogger('bfmc.laneDetection.laneDetectionThread.edgeDetection')

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

    def _show_the_output(self, image, title):
        cv2.imshow(title, image)

    def _detect_line_segments(self, cropped_img):
        # GENERATING THE LINES USING HOUGH TRANSFORM
        # rho is the distance precision in pixel.
        # angle is angular precision in radian.
        # min_threshold is the number of votes needed to be considered a line segment
        # minLineLength is the minimum length of the line segment in pixels.
        # maxLineGap is the maximum in pixels that two line segments that can be separated and still be considered a single line segment.
        # CHANGE THE rho, theta, threshold, minLineLength, and maxLineGap
        line_segments = cv2.HoughLinesP(cropped_img,
                                        rho=2,
                                        theta=np.pi / 180,
                                        threshold=100,
                                        lines=np.array([]),
                                        minLineLength=100,
                                        maxLineGap=50
                                        )
        # line_segments = cv2.HoughLinesP(cropped_img,
        #                                 rho=6,
        #                                 theta=np.pi / 60,
        #                                 threshold=160,
        #                                 lines=np.array([]),
        #                                 minLineLength=40,
        #                                 maxLineGap=25
        #                                 )

        return line_segments

    def _region_of_interest(self, img):

        height = img.shape[0]
        width = img.shape[1]

        vertices = np.array([
            [(0, height), (0, height * (1 / 2)), (width / 2, height / 3), (width, height * (1 / 2)), (width, height)]
        ], dtype=np.int32)
        mask = np.zeros_like(img)
        # The number of color channels
        #    channel_count = img.shape[2]
        match_mask_color = 255
        cv2.fillPoly(mask, vertices, match_mask_color)
        masked_image = cv2.bitwise_and(img, mask)
        return masked_image

    # CANNY EDGE DETECTION
    def _cannyedge(self, img):
        gray_image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        blur_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        return cv2.Canny(blur_image, 50, 150)

    # DRAW THE GENERATED LINES ON THE IMAGE
    def _draw_lines(self, img, lines_1, color=[0, 0, 255], thickness=5):
        if lines_1 is None:
            return

        img = np.copy(img)

        line_img = np.zeros(
            (
                img.shape[0],
                img.shape[1],
                3
            ),
            dtype=np.uint8,
        )

        for line in lines_1:
            for x1, y1, x2, y2 in line:
                cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)
        img = cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)
        return img

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


        # TODO update the method from lane detection script
        # in particolare non saprei se questo triangolo è la cosa migliore da passare

        # self._printImageOnScreen(image)

        # convert the image in grays cale and than extract the region of interest
        canny_image = self._cannyedge(image)
        cropped_image = self._region_of_interest(canny_image)

        cv2.imshow("cropped image", self._region_of_interest(self._cannyedge(image)))

        # cv2.imwrite('./debug/image.png', cropped_image)
        #self._printImageOnScreen(cropped_image)

        # generate lines using the hough transform
        line_segments = self._detect_line_segments(cropped_image)

        # CREATING A SINGLE LEFT AND RIGHT LANE
        # GROUPING THE LINES INTO TWO LANE LINES, LEFT AND RIGHT GROUPS

        lanes = []
        left_line_x = []
        left_line_y = []
        right_line_x = []
        right_line_y = []

        # this part of the code detect only right and left lane marker
        boundary = 1 / 3
        left_region_boundary = image.shape[1] * (
                    1 - boundary)  # left lane line segment should be on left 2/3 of the screen
        right_region_boundary = image.shape[1] * boundary  # right lane line segment should be on left 2/3 of the screen

        if line_segments is not None:
            for line in line_segments:
                for x1, y1, x2, y2 in line:
                    slope = (y2 - y1) / (x2 - x1)

                    if math.fabs(slope) < 0.5:
                        continue

                    if slope < 0:
                        if x1 < left_region_boundary and x2 < left_region_boundary:
                            left_line_x.extend([x1, x2])
                            left_line_y.extend([y1, y2])
                    else:
                        if x1 > right_region_boundary and x2 > right_region_boundary:
                            right_line_x.extend([x1, x2])
                            right_line_y.extend([y1, y2])
        else:
            return image

        min_y = int(image.shape[0] * (1 / 2))
        max_y = image.shape[0]

        if len(left_line_x) != 0:
            poly_left = np.poly1d(np.polyfit(
                left_line_y,
                left_line_x,
                deg=1
            ))
            left_x_start = int(poly_left(max_y))
            left_x_end = int(poly_left(min_y))
            self.left_lanes.append(self._fitLane(left_line_x, left_line_y, max_y, min_y))
        else:
            left_x_start = 0
            left_x_end = 0
        lanes.append([[left_x_start, max_y, left_x_end, min_y]])

        if len(right_line_x) != 0:
            poly_right = np.poly1d(np.polyfit(
                right_line_y,
                right_line_x,
                deg=1
            ))
            right_x_start = int(poly_right(max_y))
            right_x_end = int(poly_right(min_y))
            self.right_lanes.append(self._fitLane(right_line_x, right_line_y, max_y, min_y))
        else:
            right_x_start = 0
            right_x_end = 0
        lanes.append([[right_x_start, max_y, right_x_end, min_y]])

        if len(right_line_x) == 0 and len(left_line_x) == 0:
            line_image = self._draw_lines(
                image,
                [[
                    [left_x_start, max_y, left_x_end, min_y],
                    [right_x_start, max_y, right_x_end, min_y],
                ]],
                thickness=5,
            )
        elif len(left_line_x) == 0 and len(right_line_x) != 0:
            line_image = self._draw_lines(
                image,
                [[
                    [left_x_start, 0, left_x_end, 0],
                    [right_x_start, max_y, right_x_end, min_y],
                ]],
                thickness=5,
            )
        elif len(left_line_x) != 0 and len(right_line_x) == 0:
            line_image = self._draw_lines(
                image,
                [[
                    [left_x_start, max_y, left_x_end, min_y],
                    [right_x_start, 0, right_x_end, 0],
                ]],
                thickness=5,
            )
        else:
            line_image = self._draw_lines(
                image,
                [[
                    [left_x_start, max_y, left_x_end, min_y],
                    [right_x_start, max_y, right_x_end, min_y],
                ]],
                thickness=5,
            )

        cv2.imshow("output", line_image)

        if len(left_line_x) == 0:
            self.logger.debug('we cannot detect left lanes')

        if len(right_line_y) == 0:
            self.logger.debug('we cannot detect right lanes')

        if (len(left_line_x) == 0) or (len(right_line_x) == 0):
            self.lane_detected = False
            return False

        # self.left_lanes.append(self._fitLane(left_line_x, left_line_y, max_y, min_y))
        # self.right_lanes.append(self._fitLane(right_line_x, right_line_y, max_y, min_y))
        self.lane_detected = True
        self.last_dts = ts

        return True
