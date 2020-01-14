from src.utils.templates.workerprocess import WorkerProcess
from src.data-acquisition.sensordataacquirer import SensorDataAcquirer

class SensorDataHandler(WorkerProcess):

    def __init__(self, inPs, outPs):
        # TODO check if this process should be considered a daemon process
        super(SensorDataHandler, self).__init__(inPs, outPs)


    def _init_threads(self):
        # in this method add the different threads contained into this process
        self.threads.append(SensorDataAcquirer(inPs))

    # this method is used to initialize the sensor data handler before reading the information from the sensor handler process
    def run(self): 


    def stop(self)
    