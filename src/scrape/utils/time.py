import datetime


class TimeUtils:
    epoch = datetime.datetime(1970, 1, 1)

    @staticmethod
    def unix_time():
        delta = datetime.datetime.now() - TimeUtils.epoch
        return delta.total_seconds()

    @staticmethod
    def unix_time_mills():
        return int(round(TimeUtils.unix_time() * 1000,0))

    @staticmethod
    def string_to_unix_time_mills(string):
        converted_time = datetime.datetime.strptime(string, '%Y-%m-%d')
        return int(round((converted_time    - TimeUtils.epoch).total_seconds() * 1000,0))

    @staticmethod 
    def unix_time_mills_to_string(mills):
        return datetime.datetime.fromtimestamp(mills/1000.0)

