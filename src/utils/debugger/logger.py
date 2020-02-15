import os

from datetime import date
from datetime import datetime
from pathlib import Path


class ProjectLogger:

    def __init__(self, logfilename):
        self.logfilename = logfilename
        self.debug_dir = Path('./debug')

        if not self.debug_dir.exists():
            os.mkdir(self.debug_dir.as_posix())

        today = date.today().strftime('%d-%m-%Y')
        now = datetime.now().strftime('%H:%M:%S')

        dir_name = "debug_" + today + "_" + now

        self.current_debug_dir = self.debug_dir / dir_name
        os.mkdir(self.current_debug_dir)
        os.chdir(self.current_debug_dir)

        # open a new logfile
        self.log_file = open(self.logfilename, "w")

    def write_log(self, class_name, line):
        today = date.today().strftime('%d-%m-%Y')
        now = datetime.now().strftime('%H:%M:%S')
        timestamp = today + " " + now
        s = "[{c}] ({t}) {l}".format(c=class_name, t=timestamp, l=line)
        self.log_file.write(s)

    def close_log(self):
        self.log_file.close()


