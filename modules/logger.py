import json
import os
import time
from modules.constants import LOG_DIRECTORY, GENERAL_CONFIG_FILE, KEEP_LOGS

class Logger():
    logger = None
    def __init__(self):
        if not Logger.logger:
            Logger.logger = Logger.__Logger()

    def __getattr__(self, name):
        return getattr(self.logger, name)

    class __Logger():
        def __log_path(self, exporter_id):
            timestamp = time.strftime("%Y%m%dT%H%M%S", time.localtime())
            return "{}/{}_{}.log".format(LOG_DIRECTORY, timestamp, exporter_id)

        def __delete_old(self, exporter_id):
            exporter_logs = []
            for log in os.listdir(LOG_DIRECTORY):
                if exporter_id in log:
                    exporter_logs.append(os.path.join(LOG_DIRECTORY, log))
            delete_logs = exporter_logs[:-KEEP_LOGS]
            for log in delete_logs:
                os.remove(log)
            return None

        def set_path(self, exporter_id):
            self.log_path = self.__log_path(exporter_id)
            open(self.log_path, "w").close()
            self.__delete_old(exporter_id)

        def log(self, text):
            with open(self.log_path, "a") as log_file:
                log_file.write(text + "\n")
