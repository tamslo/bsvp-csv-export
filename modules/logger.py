import time
from modules.constants import LOG_DIRECTORY

class Logger():
    logger = None
    def __init__(self):
        if not Logger.logger:
            Logger.logger = Logger.__Logger()

    def __getattr__(self, name):
        return getattr(self.logger, name)

    class __Logger():
        def set_path(self, exporter_id):
            timestamp = time.strftime("%Y%m%dT%H%M%S", time.localtime())
            self.log_path = ("{}/{}_{}.log".format(LOG_DIRECTORY, timestamp, exporter_id))
            open(self.log_path, "w").close()

        def log(self, text):
            with open(self.log_path, "a") as log_file:
                log_file.write(text + "\n")
