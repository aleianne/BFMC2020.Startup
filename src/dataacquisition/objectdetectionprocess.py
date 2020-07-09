from src.utils.templates.workerprocess import WorkerProcess
from src.dataacquisition.signdetectionthread import SignDetectionThread

import logging


class ObjectDetectionProcess(WorkerProcess):

    def __init__(self, inPs, outPs):
        super(ObjectDetectionProcess, self).__init__(inPs, outPs)
        self.logger = logging.getLogger("bfmc.objectDetection")

    def _init_threads(self):
        if len(self.inPs) != 1:
            self.logger.error("Wrong number of input connections")
            return

        if len(self.outPs) != 0:
            self.logger.error("Wrong number of output connections")
            return

        # this process should have a single input connection and a single output connection
        self.in_conn = self.inPs[0]

        self.threads.append(SignDetectionThread(self.in_conn))
