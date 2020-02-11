from src.utils.debugger.debugger import Debugger


class CameraDebugger(Debugger):

    def __init__(self, logfilename):
        super(CameraDebugger, self).__init__(logfilename)
        self.frame_stream = None

        # here we need to open the stream

    def write_frame(self, img):
        pass

    def close_stream(self):
        pass

    # with this method i can close the entire debugging session
    def end_debug(self):
        self.close_log()
        self.close_stream()
