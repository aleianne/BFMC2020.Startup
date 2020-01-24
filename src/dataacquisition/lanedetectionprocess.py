# This class is in charge of collecting the information coming from the
# Camera handler process and parsing in it in order to be manipulated. 
# In this way is possible to apply all the lane detection algorithm 

from src.utils.templates.workerprocess import WorkerProcess
from src.dataacquisition.cameraacquirer import CameraAcquirer
from src.dataacquisition.testcmdthread import TestCmdThread

from threading import Thread

class LaneDetectionProcess(WorkerProcess): 

    def __init__(self, inPs, outPs): 
        super(LaneDetectionProcess, self).__init__(inPs, outPs)

    def _init_threads(self): 

        if len(self.inPs) != 1: 
            print("LaneDetectionProcess: no input connection has been specified")
            return 

        if len(self.outPs) != 1:
            print("LaneDetectionProcess: no output connection has been specified")
            return

        self.inConn = self.inPs[0]
        self.outConn = self.outPs[0]

        self.threads.append(CameraAcquirer(self.inConn))

        #self.threads.append(TestCmdThread(self.outPs))