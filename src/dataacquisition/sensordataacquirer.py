from src.utils.templates.workerthread import ThreadWithStop


# per il momento non lo so se questo thread a bisogno di avere un metodo stop quando viene chiuso
class SensorDataAcquirer(ThreadWithStop):
    
    def __init__(self, inPs)
        super(SensorDataAcquirer, self).__init__()
        self.inPs = inPs


    def run(self):

    def stop(self):