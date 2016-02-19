import io
import gzip
import datetime

from scrape.crawl.ftp import Ftp
from scrape.handlers.text import Text


class CustomHandler:
    @staticmethod
    def get_report(path):
        opts = dict()
        opts['url'] = 'ftp.sec.gov'
        opts['paths'] = [path]
        opts['handler'] = Text.to_stdout
        Ftp(opts).run()

    @staticmethod
    def to_stdout(sio):
        reader = io.BufferedReader(gzip.GzipFile(fileobj=sio))
        with io.TextIOWrapper(reader, encoding="ISO-8859-1") as file:
            for line in file:
                if not CustomHandler.is_report_line(line):
                    continue
                parsedLine = CustomHandler.parse_line(line)
                print(parsedLine, end='')
                print()
                CustomHandler.get_report(parsedLine['path'])
            file.close()

    @staticmethod
    def is_report_line(line):
        return line.__contains__("|edgar/data")

    @staticmethod
    def parse_line(line):
        split = line.split('|')
        parsed = dict()
        parsed['cik'] = split[0]
        parsed['reportType'] = split[2]
        parsed['fileDate'] = split[3]
        parsed['path'] = split[4].strip('\n')
        return parsed

opts = dict()
opts['url'] = 'ftp.sec.gov'
opts['paths'] = [
        '/edgar/full-index/'+str(year)+'/QTR'+str(qtr)+'/master.gz'
        for year in range(1993, datetime.date.today().year)
        for qtr in range(1,4+1)
    ]
opts['handler'] = CustomHandler.to_stdout
Ftp(opts).run()

