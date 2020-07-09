from pathlib import Path
from datetime import date
from datetime import datetime
from src.utils.singleton import Singleton

import os
import logging


class InitLogger(metaclass=Singleton):

    def __init__(self):
        self.filename = "application.log"
        self.debug_dir = Path('./debug')
        self.current_debug_dir = None

        self._createDebugDir()

        # create a new file handler for the logger
        file_path = self.current_debug_dir / self.filename
        file_handler = logging.FileHandler(str(file_path))
        file_handler.setLevel(logging.DEBUG)

        # create a new formatter for the logger
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # create a new logger
        self.logger = logging.getLogger('bfmc')
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.DEBUG)

    def _createDebugDir(self):
        today = date.today().strftime('%d_%m_%Y')
        now = datetime.now().strftime('%H_%M_%S')
        dir_name = "debug_" + today + "_" + now

        if not self.debug_dir.exists():
            os.mkdir(str(self.debug_dir))

        self.current_debug_dir = self.debug_dir / dir_name
        os.mkdir(str(self.current_debug_dir))

    def getDebugDir(self):
        return self.current_debug_dir
