import gzip
import io

from ..utils.time import TimeUtils


class Gzip:
    @staticmethod
    def to_stdout(sio):
        with io.TextIOWrapper(io.BufferedReader(gzip.GzipFile(fileobj=sio))) as file:
            for line in file:
                print(line)
            file.close()

    @staticmethod
    def to_txt(sio):
        out = open(str(TimeUtils.unix_time_mills())+"_report.txt", "wt")
        with io.TextIOWrapper(io.BufferedReader(gzip.GzipFile(fileobj=sio))) as file:
            for line in file:
                out.write(line)
        out.close()
        file.close()
