from cv2 import cv2
import numpy as np

img = cv2.imread('C:\\Users\\xiangbo\\Desktop\\4.jpg', 1)
print('img:', type(img), img.shape, img.dtype)
cv2.namedWindow('img', cv2.WINDOW_NORMAL)

cv2.imshow('img', img)
# RGB to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow('hsv', hsv)

# select blue traffic sign
blue_lower = np.array([100, 50, 50])
blue_upper = np.array([124, 255, 255])
# mask
mask = cv2.inRange(hsv, blue_lower, blue_upper)
print('mask', type(mask), mask.shape)
cv2.imshow('mask', mask)

# reducing noise
# blur
blurred = cv2.blur(mask, (9, 9))
cv2.imshow('blurred', blurred)

# binarization
ret, binary = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
cv2.imshow('blurred binary', binary)

# closed
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
cv2.imshow('closed', closed)

# erode and dilate
erode = cv2.erode(closed, None, iterations=4)
cv2.imshow('erode', erode)
dilate = cv2.dilate(erode, None, iterations=4)
cv2.imshow('dilate', dilate)

contours, hierarchy = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print('the number of contours：', len(contours))
i = 0
res = img.copy()
for con in contours:

    rect = cv2.minAreaRect(con)
    # box
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    # the segmation area on original image
    cv2.drawContours(res, [box], -1, (0, 0, 255), 2)
    print([box])
    # the dimension of matrix
    h1 = min(box.max(axis=0))
    h2 = min(box.min(axis=0))
    l1 = max(box.max(axis=1))
    l2 = min(box.max(axis=1))
    print('h1', h1)
    print('h2', h2)
    print('l1', l1)
    print('l2', l2)
    # make sure if the area is accurate
    if h1 - h2 > 0 and l1 - l2 > 0:
        # segmentation
        temp = img[h2:h1, l2:l1]
        i = i + 1
        # show the image sign
        cv2.imshow('sign' + str(i), temp)
        # turn it into 40*40
        atemp = cv2.resize(temp, (40, 40), interpolation=cv2.INTER_CUBIC)
        cv2.imshow('aftersign' + str(i), atemp)

# show the initial image with marked sign
cv2.imshow('res', res)

# ues esc to close
k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()
