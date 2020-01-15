from src.utils.templates.workerprocess import WorkerProcess
from src.dataacquisition.sensordataacquirer import SensorDataAcquirer

class SensorDataHandler(WorkerProcess):

    def __init__(self, inPs, outPs):
        # TODO check if this process should be considered a daemon process
        super(SensorDataHandler, self).__init__(inPs, outPs)

    def _init_threads(self):
        # in this method add the different threads contained into this process
        self.threads.append(SensorDataAcquirer(self.inPs, self.outPs))