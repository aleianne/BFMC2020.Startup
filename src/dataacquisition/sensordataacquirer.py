from src.utils.templates.workerthread import WorkerThread

# per il momento non lo so se questo thread a bisogno di avere un metodo stop quando viene chiuso
class SensorDataAcquirer(WorkerThread):
    
    def __init__(self, inPs, outPs):
        super(SensorDataAcquirer, self).__init__(inPs, outPs)
        self._running = True

    def _init_threads(self):
        pass

    def run(self):
        # check if the incoming connection is only one
        if len(self.inPs) != 1: 
            print("SensorDataAcquirer should have only one icoming pipe")
            return

        inConn = self.inPs[0]    
        while self._running: 
            try:
                data = pipe.recv()
                if type(data) == "str":
                    print("Data received from the Serial Handle" + data)
                else: 
                    print("Data type received is "+ type(data)) 
            except Exception:
                #print("SensorDataAcquirer raised an exception")       
                pass