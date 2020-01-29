from src.utils.templates.threadwithstop import ThreadWithStop
from src.dataacquisition.imageprocessing.edgedetection import EdgeDetection
from src.dataacquisition.imageprocessing.lanetracking import LaneTracking

import cv2


class CameraAcquirer(ThreadWithStop):

    def __init__(self, in_conn):
        super(CameraAcquirer, self).__init__()
        self.in_conn = in_conn

        # define the lane tracker object
        self.right_lane_tracker = LaneTracking()
        self.left_lane_tracker = LaneTracking()

        # define the edge detector object
        self.edge_detection = EdgeDetection()

        self.last_ts = None                     # last frame timestamp
        self.last_dts = None                    # last frame with lane detected timestamp

    def run(self):

        while self._running:
            try: 
                # iterate all over the possible incoming connections
                data_read = self.in_conn.recv()
                time = data_read[0][0]
                image = data_read[1]

                # before any computation, convert the frame in gray scale
                # in this way we can reach a better edge detection
                gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

                if not self.edge_detection.getLaneDetected:
                    self.edge_detection.laneDetection(gray_image)

                    left_lane = self.edge_detection.getLastDetectedLLane()
                    right_lane = self.edge_detection.getLastDetectedRLane()

                    if left_lane is not None:
                        self.left_lane_tracker.setLane(left_lane)

                    if right_lane is not None:
                        self.right_lane_tracker.setLane(right_lane)

                else: 
                    # before the actual tracking operation, we need to apply canny edge detector
                    edges_img = cv2.Canny(gray_image, 100, 200)

                    self.right_lane_tracker.trackLane(edges_img)
                    self.left_lane_tracker.trackLane(edges_img)

                # update the last timestamp
                self.last_ts = time

            except EOFError:
                print("CameraAcquirer: the incoming connection has been closed")
                self._running = False

    def stop(self):
        self._running = False
