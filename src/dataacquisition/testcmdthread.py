from src.utils.templates.threadwithstop import ThreadWithStop
from threading import Thread

import time

class TestCmdThread(ThreadWithStop):

    def __init__(self, outPs):
        super(ThreadWithStop, self).__init__()
        self.outPs = outPs

    def run(self): 
        # create a command to start the car 
        start      = {"action": "MCTL", "speed": 0.21, "steerAngle": 5.0}
        stop       = {"action": "BRAK", "steerAngle": 20.0}

        stop_array = [
            {"action": "MCTL", "speed": 0.30, "steerAngle": 30.0},
            {"action": "BRAK", "steerAngle": 30.0},
            {"action": "BRAK", "steerAngle": -30.0},
            {"action": "BRAK", "steerAngle": 15.0},
            {"action": "BRAK", "steerAngle": -15.0}, 
            {"action": "BRAK", "steerAngle": 0.0}  
        ]
           
        if len(self.outPs) == 1: 
            pipe = self.outPs[0]
            
            for s in stop_array:
                time.sleep(2)
                pipe.send(s)
                print("I'm steering of " + str(s["steerAngle"]) + " degree")
        else:
            print("in Lane Detection there are more than 1 output connection")