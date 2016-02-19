from ..utils.time import TimeUtils


class LogUtils:

    @staticmethod
    def log_info(message):
        print('[{0}] Info: {1} '.format(TimeUtils.unix_time_mills(), message))

    @staticmethod
    def log_error(message):
        print('[{0}] Error: {1} '.format(TimeUtils.unix_time_mills(), message))

