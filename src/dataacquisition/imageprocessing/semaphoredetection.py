import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import numpy as np
from enum import Enum
import logging

class TLState(Enum):
    red = 1
    yellow = 2
    green = 3


class SemaphoreDetection:
    def __init__(self):
        # define the lower and upper bound for the colors
        self.red_min = np.array([0, 5, 150])
        self.red_max = np.array([8, 255, 255])
        self.red_min2 = np.array([175, 5, 150])
        self.red_max2 = np.array([180, 255, 255])

        self.yellow_min = np.array([20, 5, 150])
        self.yellow_max = np.array([30, 255, 255])

        self.green_min = np.array([35, 5, 150])
        self.green_max = np.array([90, 255, 255])

        self.light_path = []    #"images/4.jpg", "images/5.png", "images/2.png", "images/6.jfif"


        self.BoI = []              #(list?)

        self.object_detected = False

        self.logger = logging.getLogger("bfmc.objectDetection.signDetectionThread.imageSegmentation")

    def getObjectDetected(self):      #定义此方法判断是否检测到物体，返回真假
        if len(self.BoI) > 0:
            return True
        else:
            return False

    def getBlobOfInterst(self):        #定义想要识别的目标方法，返回list
        return self.BoI

    def detectColor(self, image):  # receives an ROI containing a single light
        # convert RGB image to HSV
        hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # apply red, yellow, green thresh to image
        # Mask 利用cv2.inRange函数设阈值，去除背景部分
        red_thresh = cv2.inRange(hsv_img, self.red_min, self.red_max) + cv2.inRange(hsv_img, self.red_min2, self.red_max2)
        yellow_thresh = cv2.inRange(hsv_img, self.yellow_min, self.yellow_max)
        green_thresh = cv2.inRange(hsv_img, self.green_min, self.green_max)


        # apply blur to fix noise in thresh

        red_blur = cv2.medianBlur(red_thresh, 5)
        yellow_blur = cv2.medianBlur(yellow_thresh, 5)
        green_blur = cv2.medianBlur(green_thresh, 5)

        # checks which colour thresh has the most white pixels
        red = cv2.countNonZero(red_blur)
        yellow = cv2.countNonZero(yellow_blur)
        green = cv2.countNonZero(green_blur)

        # the state of the light is the one with the greatest number of white pixels
        lightColor = max(red, yellow, green)

        # pixel count must be greater than 60 to be a valid colour state (solid light or arrow)
        # since the ROI is a rectangle that includes a small area around the circle
        # which can be detected as yellow
        if lightColor > 60:
            if lightColor == red:
                return 1
            elif lightColor == yellow:
                return 2
            elif lightColor == green:
                return 3
        else:
            return 0

    def imgResize(self,image, height, inter=cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and grab the image size
        dim = None
        (h, w) = image.shape[:2]
        # calculate the ratio of the height and construct the dimensions
        r = height / float(h)
        dim = (int(w * r), height)
        # resize the image
        resized = cv2.resize(image, dim, interpolation=inter)
        # return the resized image
        return resized

    def detectState(self, image):
        image = self.imgResize(image, 200)
        (height, width) = image.shape[:2]
        output = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 霍夫圆环检测
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20,
                                   param1=50, param2=30, minRadius=15, maxRadius=30)
        overallState = 0
        if circles is not None:
            circles = np.uint16(np.around(circles))

            for i in circles[0, :]:
                if i[1] < i[2]:
                    i[1] = i[2]
                roi = image[(i[1] - i[2]):(i[1] + i[2]), (i[0] - i[2]):(i[0] + i[2])]
                color = self.detectColor(roi)
                if color > 0:
                    overallState = color

        return overallState

    def plot_light_result(self,images):        #it should be modified to write in videos by using camraspoofer?
        for i, image in enumerate(images):
            plt.subplot(1, len(images), i + 1)
            lena = mpimg.imread(image)
            label = self.TLState(self.detectState(cv2.imread(image))).name
            plt.title(label)
            plt.imshow(lena)
        plt.show()



#tl1 = DetectColor
#tl1.light_path = ["images/4.jpg","images/5.png", "images/2.png","images/6.jfif"]
#tl1.plot_light_result(tl1.light_path)


