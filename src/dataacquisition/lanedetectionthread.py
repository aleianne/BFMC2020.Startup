from src.utils.templates.threadwithstop import ThreadWithStop
from src.dataacquisition.imageprocessing.edgedetection import EdgeDetection
from src.dataacquisition.imageprocessing.lanetracking import LaneTracking
from src.utils.debugger.cameradebugger import CameraDebugger

import cv2


class LaneDetectionThread(ThreadWithStop):

    def __init__(self, in_conn, debug=False):
        super(LaneDetectionThread, self).__init__()
        self.in_conn = in_conn
        self.debug = debug

        if debug:
            self.camera_debugger = CameraDebugger("lane_tracking")
        else:
            self.camera_debugger = None

        # define the lane tracker object
        self.right_lane_tracker = LaneTracking(self.camera_debugger)
        self.left_lane_tracker = LaneTracking(self.camera_debugger)

        # define the edge detector object
        self.edge_detection = EdgeDetection(self.camera_debugger)

        self.lane_detected = False

        self.last_ts = None                     # last frame timestamp
        self.last_dts = None                    # last frame with lane detected timestamp

    # DEFINITION OF PRIVATE METHODS
    def _stopAcquisition(self):
        self._running = False
        if self.debug:
            self.camera_debugger.end_debug()

    # EXTEND RUN METHOD OF THREAD CLASS
    def run(self):

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

                    # check if the right and left lane has been detected by the lane tracker
                    right_lane_det = self.right_lane_tracker.trackLane(edges_img)
                    left_lane_det = self.left_lane_tracker.trackLane(edges_img)

                    # if neither the left and the right lane has been detected
                    # apply the lane detection algorithm
                    self.lane_detected = right_lane_det or left_lane_det

                    if self.debug:
                        self.camera_debugger.write_log("bla bla bla")

                else:
                    if self.edge_detection.laneDetection(gray_image):

                        left_lane = self.edge_detection.getLastDetectedLLane()
                        right_lane = self.edge_detection.getLastDetectedRLane()

                        if left_lane is not None:
                            self.left_lane_tracker.setLane(left_lane)
                            if self.debug:
                                self.camera_debugger.write_log("bla bla bla")

                        if right_lane is not None:
                            self.right_lane_tracker.setLane(right_lane)
                            if self.debug:
                                self.camera_debugger.write_log("bla bla bla")

                        self.lane_detected = True
                        self.last_dts = time
                    else:
                        #  lane detector class couldn't detect the lane markers
                        self.lane_detected = False

                # update the last timestamp
                self.last_ts = time

                if self.debug:
                    # put here the frame captured by our camera
                    pass

            except EOFError:
                print("CameraAcquirer: the incoming connection has been closed")
                self._stopAcquisition()

    def stop(self):
        self._stopAcquisition()
