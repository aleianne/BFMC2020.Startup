# This class is in charge of collecting the information coming from the
# Camera handler process and parsing in it in order to be manipulated. 
# In this way is possible to apply all the lane detection algorithm,  

from src.utils.templates.workerprocess import WorkerProcess
from src.dataacquisition.cameraacquirer import CameraAcquirer

class LaneDetector(WorkerProcess): 

    def __init__(self, inPs, outPs, daemon): 
        super(LaneDetector, self).__init__(inPs, outPs)

    def _init_threads(self): 
      self.threads.append = CameraAcquirer(inPs, outPs)

        


    
    

