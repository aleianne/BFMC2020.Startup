# This class is in charge of collecting the information coming from the
# Camera handler process and parsing in it in order to be manipulated. 
# In this way is possible to apply all the lane detection algorithm 

from src.utils.templates.workerprocess import WorkerProcess
from src.dataacquisition.lanedetectionthread import LaneDetectionThread
from src.dataacquisition.testcmdthread import TestCmdThread

from queue import Queue
from threading import Condition

import logging


class LaneDetectionProcess(WorkerProcess): 

    def __init__(self, inPs, outPs): 
        super(LaneDetectionProcess, self).__init__(inPs, outPs)

        # define queue
        self.lane_queue = Queue(20)

        # define the logger class
        self.logger = logging.getLogger("bfmc.laneDetection")

        # create a condition variable
        self.cv = Condition()

    def _init_threads(self): 

        if len(self.inPs) != 1: 
            self.logger.error("Wrong number of input connections")
            return 

        if len(self.outPs) != 1:
            self.logger.error("Wrong number of output connections")
            return

        self.in_conn = self.inPs[0]
        self.out_conn = self.outPs[0]

        self.threads.append(LaneDetectionThread(self.in_conn, self.lane_queue, self.cv))
        #self.threads.append(TestCmdThread(self.outPs))
