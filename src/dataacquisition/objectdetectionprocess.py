from src.utils.templates.workerprocess import WorkerProcess

class ObjectDetectionProcess(WorkerProcess):

    def __init__(self, inPs, outPs):
        super(ObjectDetection, self).__init(inPs, outPs)

    def _init_threads(self):
        self.threads.append()

    