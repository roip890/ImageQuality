from enum import Enum
from utils.terminal_colors import terminal_colors


class Logger(object):
    def __init__(self, log_file_name):
        self.log_file_name = log_file_name

    def log(self, log_text, logger_color=None):
        if logger_color is not None:
            print(f'{logger_color}{log_text}{terminal_colors.ENDC}')
        else:
            print(f'{log_text}')
        with open(self.log_file_name, 'a+') as log_file:
            log_file.write(f'{log_text}\n')
