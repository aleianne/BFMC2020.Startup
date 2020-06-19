from src.utils.templates.threadwithstop import ThreadWithStop
from src.dataacquisition.imageprocessing.edgedetection import EdgeDetection
from src.dataacquisition.imageprocessing.lanetracking import LaneTracking
from src.utils.debugger.videologger import VideoLogger
import logging

import cv2


class LaneDetectionThread(ThreadWithStop):

    def __init__(self, in_conn, out_queue, cv, video_debug=False):
        super(LaneDetectionThread, self).__init__()
        self.in_conn = in_conn
        self.out_queue = out_queue

        # store the condition variable inside this thread
        # this variable should be used to synchronize the access to the queue
        self.cv = cv

        # define the logger
        self.logger = logging.getLogger("bfmc.laneDetection.laneDetectionThread")
        self.video_debug = video_debug

        if video_debug:
            self.cameraDebugger = VideoLogger()

        # define the lane tracker object
        self.right_lane_tracker = LaneTracking()
        self.left_lane_tracker = LaneTracking()

        # define the edge detector object
        self.edge_detection = EdgeDetection()

        self.lane_detected = False

        self.last_ts = None                     # last frame timestamp

    # DEFINITION OF PRIVATE METHODS
    def _stopAcquisition(self):
        self.logger.debug("Forced the interruption of computation")
        self._running = False

    def _writeOutputData(self, data):
        with self.cv:
            self.out_queue.put(data)
            self.cv.notify()

    # EXTEND RUN METHOD OF THREAD CLASS
    def run(self):

        self.logger.info("Started lane detection")

        while self._running:
            try: 
                data_read = self.in_conn.recv()
                time = data_read[0][0]
                image = data_read[1]

                # frame conversion in gray scale
                gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

                if self.lane_detected:

                    # before the actual tracking operation, we need to apply canny edge detector
                    edges_img = cv2.Canny(gray_image, 100, 200)

                    # check if the right and left lane have been detected by the lane tracker
                    right_lane_det = self.right_lane_tracker.trackLane(edges_img)
                    left_lane_det = self.left_lane_tracker.trackLane(edges_img)

                    # if neither left and right lane has been detected
                    # apply the lane detection algorithm
                    self.lane_detected = right_lane_det and left_lane_det
                    #self._writeOutputData(self.lane_detected)

                    if self.lane_detected:
                        self.logger.debug("Lane tracking...")
                    else:
                        self.logger.debug("Impossible to track left and right lanes")

                else:
                    self.edge_detection.initDetection()
                    if (self.edge_detection.laneDetection(image, time)).any():

                        left_lane = self.edge_detection.getLastDetectedLLane()
                        right_lane = self.edge_detection.getLastDetectedRLane()

                        self.left_lane_tracker.setLane(left_lane)
                        self.right_lane_tracker.setLane(right_lane)

                        self.logger.debug("Lane detected correctly!")

                        self.lane_detected = True
                    else:
                        # lane detector class couldn't detect the lane markers
                        self.logger.debug("No lanes has been detected")
                        self.lane_detected = False

                # update the last timestamp
                self.last_ts = time

            except EOFError:
                self.logger.debug("Input connection has been closed")
                self._stopAcquisition()

    def stop(self):
        self._stopAcquisition()
