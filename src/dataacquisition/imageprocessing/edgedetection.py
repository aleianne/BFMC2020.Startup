import cv2
import math
import numpy as np


class EdgeDetection:

    def __init__(self):
        self.right_lane_x = []
        self.left_lane_x = []

        self.right_lane_y = []
        self.left_lane_y = []

        self.lane_detected = False

    # DEFINITION OF GET/SET METHODS

    def getRightLaneX(self):
        return self.right_lane_x

    def getRightLaneY(self):
        return self.right_lane_y

    def getLeftLaneX(self):
        return self.left_lane_x

    def getLeftLaneY(self):
        return self.left_lane_y

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

        # convert the image in grayscale and than extract the region of interest
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        canny_image = self._cannyEdge(gray_image)
        cropped_image = self._regionOfInterest(
            canny_image,
            np.array([region_of_interest_vertices], np.int32),
        )

        # generate the lines using the hough transform
        line_segments = self._detectLineSegments(cropped_image)

        for line in line_segments:
            for x1, y1, x2, y2 in line:
                slope = (y2 - y1) / (x2 - x1)

                if math.fabs(slope) < 0.5:
                    continue

                if slope <= 0:
                    self.left_lane_x.extend([x1, x2])
                    self.left_lane_y.extend([y1, y2])
                else:
                    self.right_lane_x.extend([x1, x2])
                    self.right_lane_y.extend([y1, y2])

        min_y = int(image.shape[0] * (3 / 5))
        max_y = image.shape[0]

        poly_left = np.poly1d(np.polyfit(
            self.left_lane_y,
            self.left_lane_x,
            deg=1
        ))

        left_x_start = int(poly_left(max_y))
        left_x_end = int(poly_left(min_y))

        poly_right = np.poly1d(np.polyfit(
            self.right_lane_y,
            self.right_lane_x,
            deg=1
        ))

        # right_x_start = int(poly_right(max_y))
        # right_x_end = int(poly_right(min_y))
        #
        # return line_image
