from src.utils.templates.workerthread import WorkerThread
#from src.dataacquisition.detection import lane_detector

class CameraAcquirer(WorkerThread):

    def __init__(self, inPs, outPs):
    	super(CameraAcquirer, self).__init__(inPs, outPs)
    
    # This method initialize thread
    def _init_threads(self):
    	pass

    def run(self):
        while True:
            try: 
                for in_connection in self.inPs:
                    # iterate over all the possible pipe incoming into the process
                    data_read = in_connection.recv()
                    time = data_read[0][0]
                    image = data_read[1]
                    print("Image timestamp " + str(time))
                    # this function should return the information about the lane detected on the floor
                    # lane_detector(image)  
            except EOFError:
            	# TODO remember to add a stack trace in this way i can check the correct trace of the exception 
                print("CameraAcquirer: the incoming connection has been closed")
                return
