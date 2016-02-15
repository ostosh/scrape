import gzip
import io

from ..utils.time import TimeUtils


class Gzip:
    @staticmethod
    def to_stdout(sio):
        reader = io.BufferedReader(gzip.GzipFile(fileobj=sio))
        with io.TextIOWrapper(reader, encoding="ISO-8859-1") as file:
            for line in file:
                print(line, end='')
            file.close()

    @staticmethod
    def to_txt(sio):
        out = open(str(TimeUtils.unix_time_mills())+"_report.txt", "wt")
        reader = io.BufferedReader(gzip.GzipFile(fileobj=sio))
        with io.TextIOWrapper(reader, encoding="ISO-8859-1") as file:
            for line in file:
                out.write(line)
        out.close()
        file.close()
