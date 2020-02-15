from pathlib import Path
from datetime import date
from datetime import datetime

import os

import logging


class InitLogger:

    def __init__(self):
        self.filename = "application.log"
        self.debug_dir = Path('./debug')

        today = date.today().strftime('%d-%m-%Y')
        now = datetime.now().strftime('%H:%M:%S')

        self.dir_name = "debug_" + today + "_" + now

        if not self.debug_dir.exists():
            os.mkdir(self.debug_dir.as_posix())

        current_debug_dir = self.debug_dir / self.dir_name
        os.mkdir(current_debug_dir.as_posix())

        file_path = current_debug_dir / self.filename

        # create a new file handler for the logger
        file_handler = logging.FileHandler(file_path.as_posix())
        file_handler.setLevel(logging.DEBUG)

        # create a new formatter for the logger
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # create a new logger
        self.logger = logging.getLogger('bfmc')
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.DEBUG)

    def getFilename(self):
        return self.filename

    def getDebugDir(self):
        return self.debug_dir

    def getDirName(self):
        return self.dir_name
