from src.utils.templates.workerthread import WorkerThread
from src.dataacquisition.detection import lane_detector

class CameraAcquirer(WorkerThread):

    def __init__(self, inPs, outPs):
      super(CameraAcquirer, self).__init__(inPs, outPs)
    
    # This method initialize the thread
    def _init_threads(self):
      pass


    # This method override the method supplied by the thread class
    def run(self):

        # this method is in charge of receving the information from the camera
        while True:
            try: 
                for in_connection in inPs:
                    # iterate over all the possible pipe incoming into the process

                    data_read = in_connection.recv()
                    time = data_read[0]
                    image = data_read[1]

                    # this function should return the information about the lane detected on the floor
                    lane_detector(image)
                    
            except Exception: e
                # TODO remember to add a stack trace in this way i can check the correct trace of the exception 
                print(e)
