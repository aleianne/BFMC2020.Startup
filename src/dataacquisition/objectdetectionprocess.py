from src.utils.templates.workerprocess import WorkerProcess
from src.dataacquisition.signdetectionthread import SignDetectionThread


class ObjectDetectionProcess(WorkerProcess):

    def __init__(self, inPs, outPs):
        super(ObjectDetectionProcess, self).__init__(inPs, outPs)
        self.class_name = ObjectDetectionProcess.__name__

    def _init_threads(self):
        if len(self.inPs) != 1:
            print("{c}: no input connection has been specified".format(c=self.class_name))
            return

        if len(self.outPs) != 1:
            print("{c}: no output connection has been specified".format(c=self.class_name))
            return

        self.inConn = self.inPs[0]
        self.outConn = self.outPs[0]

        self.threads.append(SignDetectionThread(self.inConn))
