import cv2
import numpy as np

class EdgeDetection():

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


  # DEFINITION OF PUBLIC METHODS

  def laneDetection(self, image):
    region_of_interest_vertices = [
        (0, image.shape[0]),
        (image.shape[1] / 2, image.shape[0] / 2),
        (image.shape[1], image.shape[0]),
    ]

    # convert the image in grayscale and than extract the region of interest
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    canny_image = _cannyEdge(gray_image)
    cropped_image = _regionOfInterest(
        canny_image,
        np.array([region_of_interest_vertices], np.int32),
    )

    # generate the lines using the hughs transform
    line_segments = detect_line_segments(cropped_image)

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
        left_line_y,
        left_line_x,
        deg=1
    ))

    left_x_start = int(poly_left(max_y))
    left_x_end = int(poly_left(min_y))

    poly_right = np.poly1d(np.polyfit(
        right_line_y,
        right_line_x,
        deg=1
    ))

    right_x_start = int(poly_right(max_y))
    right_x_end = int(poly_right(min_y))

    return line_image


    # DEFINITION OF PRIVATE METHODS

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