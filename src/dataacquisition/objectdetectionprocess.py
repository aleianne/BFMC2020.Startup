from src.utils.templates.workerprocess import WorkerProcess
from src.dataacquisition.datasubscriberthread import DataSubscriberThread
from src.dataacquisition.signdetectionthread import SignDetectionThread
from src.dataacquisition.semaphoredetectionthread import SemaphoreDetectionThread
from multiprocessing import Queue
from threading import Condition

import logging


class ObjectDetectionProcess(WorkerProcess):

    def __init__(self, inPs, outPs):
        super(ObjectDetectionProcess, self).__init__(inPs, outPs)
        # set the maximum elements inside the queue as 20
        # traffic sign queue
        #self.ts_queue = Queue(20)

        self.logger = logging.getLogger("bfmc.objectDetection")



    def _init_threads(self):
        if len(self.inPs) != 1:
            self.logger.error("Wrong number of input connections")
            return

        if len(self.outPs) != 1:
            self.logger.error("Wrong number of output connections")
            return

        # this process should have a single input connection and a single output connection
        self.in_conn = self.inPs[0]
        self.out_conn = self.outPs[0]

        self.threads.append(SignDetectionThread(self.in_conn))
        self.threads.append(SemaphoreDetectionThread(self.in_conn))
        self.threads.append(DataSubscriberThread(self.out_conn))
