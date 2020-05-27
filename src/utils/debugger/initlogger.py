from pathlib import Path
from datetime import date
from datetime import datetime

import os

import logging


class InitLogger:

    def __init__(self):
        self.filename = "application.log"
        self.debug_dir = Path('./debug')

        today = date.today().strftime('%d_%m_%Y')
        now = datetime.now().strftime('%H_%M_%S')

        self.dir_name = "debug_" + today + "_" + now

        if not self.debug_dir.exists():
            os.mkdir(str(self.debug_dir))

        current_debug_dir = self.debug_dir / self.dir_name
        print(str(current_debug_dir))
        os.mkdir(str(current_debug_dir))

        file_path = current_debug_dir / self.filename

        # create a new file handler for the logger
        file_handler = logging.FileHandler(str(file_path))
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
