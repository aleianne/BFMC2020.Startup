from src.utils.templates.workerthread import ThreadWithStop

from threading import ThreadWithStop

class CameraAcquirer(ThreadWithStop):

    def __init__(self, inPs):
        super(CameraAcquirer, self).__init__()
        self.inPs = inPs
        # declare a new 

    # This method override the method supplied by the thread class
    def run(self):

        # this method is in charge of receving the information from the camera
        while True:
            try: 
                for pipe in inPs:
                    # iterate over all the possible pipe incoming into the process
                    
            except Exception: e
                # TODO remember to add a stack trace in this way i can check the correct trace of the exception 
                print(e)

    # This method override the method supplied by the ThreadWithStop class
    def stop(self):
