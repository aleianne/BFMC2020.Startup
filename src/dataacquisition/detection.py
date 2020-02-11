#from moviepy.editor import VideoFileClip

import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math

# image = mpimg.imread('road1.jpg')

# print('This image is:', type(image), 'with dimensions:', image.shape)
# plt.imshow(image)
# plt.show()

# REGION OF INTEREST
# region_of_interest_vertices = [
#     (0, image.shape[0]),
#     (image.shape[1] / 2, image.shape[0] / 3),
#     (image.shape[1], image.shape[0]),
# ]


def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    # The number of color channels
    #    channel_count = img.shape[2]
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


# CANNY EDGE DETECTION
def cannyedge(img):
    return cv2.Canny(img, 100, 200)


# DRAW THE GENERATED LINES ON THE IMAGE
def draw_lines(img, lines_1, color=[255, 0, 0], thickness=3):
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


def detect_line_segments(cropped_img):
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


# THE PIPELINE
def lane_detector(image):
    # print('This image is:', type(image), 'with dimensions:', image.shape)

    region_of_interest_vertices = [
        (0, image.shape[0]),
        (image.shape[1] / 2, image.shape[0] / 2),
        (image.shape[1], image.shape[0]),
    ]

    # CONVERT THE IMAGE TO GRAYSCALE IMAGE THEN USING CANNY EDGE TO DETECT THE EDGES AND THEN CROP THE IMAGE
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    canny_image = cannyedge(gray_image)
    cropped_image = region_of_interest(
        canny_image,
        np.array([region_of_interest_vertices], np.int32),
    )

    # GENERATING THE LINES USING HOUGH TRANSFORM
    line_segments = detect_line_segments(cropped_image)

    # CREATING A SINGLE LEFT AND RIGHT LANE
    # GROUPING THE LINES INTO TWO LANE LINES, LEFT AND RIGHT GROUPS

    left_line_x = []
    left_line_y = []
    right_line_x = []
    right_line_y = []

    for line in line_segments:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1)

            if math.fabs(slope) < 0.5:
                continue

            if slope <= 0:
                left_line_x.extend([x1, x2])
                left_line_y.extend([y1, y2])
            else:
                right_line_x.extend([x1, x2])
                right_line_y.extend([y1, y2])

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

    line_image = draw_lines(
        image,
        [[
            [left_x_start, max_y, left_x_end, min_y],
            [right_x_start, max_y, right_x_end, min_y],
        ]],
        thickness=5,
    )

    return line_image


# image = mpimg.imread('road2.jpg')
# final_image = lane_detector(image)
#
# plt.figure()
# plt.imshow(final_image)
# plt.show()

# # CONVERT THE IMAGE TO GRAYSCALE IMAGE THEN USING CANNY EDGE TO DETECT THE EDGES AND THEN CROP THE IMAGE
# gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
# cannyImg = cannyedge(gray_image)
# cropped_image = region_of_interest(
#     cannyImg,
#     np.array([region_of_interest_vertices], np.int32),
# )

# plt.figure()
# plt.imshow(cropped_image)
# plt.show()

# GENERATING THE LINES USING HOUGH TRANSFORM
# lines = cv2.HoughLinesP(cropped_image,
#                         rho=6,
#                         theta=np.pi / 60,
#                         threshold=160,
#                         lines=np.array([]),
#                         minLineLength=40,
#                         maxLineGap=25
#                         )
# # CHANGE THE rho, theta, threshold, minLineLength, and maxLineGap
# print(lines)

# GENERATING LINES AND DRAW THEM ON THE IMAGE
# line_image = draw_lines(image, lines)
# plt.figure()
# plt.imshow(line_image)
# plt.show()

# # CREATING A SINGLE LEFT AND RIGHT LANE
# # GROUPING THE LINES INTO LEFT AND RIGHT GROUPS
# left_line_x = []
# left_line_y = []
# right_line_x = []
# right_line_y = []
#
# for line in lines:
#     for x1, y1, x2, y2 in line:
#         slope = (y2 - y1) / (x2 - x1)
#
#         if math.fabs(slope) < 0.5:
#             continue
#
#         if slope <= 0:
#             left_line_x.extend([x1, x2])
#             left_line_y.extend([y1, y2])
#         else:
#             right_line_x.extend([x1, x2])
#             right_line_y.extend([y1, y2])
#
# min_y = int(image.shape[0] * (3 / 5))
# max_y = image.shape[0]
#
# poly_left = np.poly1d(np.polyfit(
#     left_line_y,
#     left_line_x,
#     deg=1
# ))
#
# left_x_start = int(poly_left(max_y))
# left_x_end = int(poly_left(min_y))
#
# poly_right = np.poly1d(np.polyfit(
#     right_line_y,
#     right_line_x,
#     deg=1
# ))
#
# right_x_start = int(poly_right(max_y))
# right_x_end = int(poly_right(min_y))
#
# line_image = draw_lines(
#     image,
#     [[
#         [left_x_start, max_y, left_x_end, min_y],
#         [right_x_start, max_y, right_x_end, min_y],
#     ]],
#     thickness=5,
# )
# plt.figure()
# plt.imshow(line_image)
# plt.show()


def test_lane_detection():
  # video1 = VideoFileClip('Lane Detection Test Video 01_input.mp4')
  video1 = VideoFileClip('solidYellowLeft.mp4')
  video_output = 'Lane Detection Test Video 01_output.mp4'
  the_result = video1.fl_image(lane_detector)
  the_result.write_videofile(video_output, audio=False)
