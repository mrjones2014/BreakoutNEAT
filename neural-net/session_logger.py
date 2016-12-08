import time
import os


class SessionLogger(object):
    def __init__(self, filename=None, do_log=False):
        self.filename = filename
        self.do_log = do_log

    def log(self, string):
        """
        Logs a timestamp and the parameter string to logfile and prints to console.
        :param string: string to log/print
        :return: void
        """
        if self.do_log:
            with open(self.filename, 'a+') as logfile:
                date_string = "[ " + time.strftime("%m/%d/%Y") + ", " + time.strftime("%I:%M:%S") + " ]:  "
                logfile.write(date_string + string + os.linesep)
        print string

    @staticmethod
    def log_metrics(filename_value_dict):
        file_names = filename_value_dict.keys()
        for filename in file_names:
            with open(filename, "a+") as curr_file:
                curr_file.write(str(filename_value_dict[filename]) + os.linesep)
