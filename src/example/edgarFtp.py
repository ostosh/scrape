import io
import gzip
import datetime
import re

from scrape.crawl.ftp import Ftp
from scrape.handlers.text import Text


class CustomHandler:
    @staticmethod
    def process_index(sio):
        reports = []
        reader = io.BufferedReader(gzip.GzipFile(fileobj=sio))
        with io.TextIOWrapper(reader, encoding="ISO-8859-1") as file:
            for line in file:
                if not CustomHandler.is_report_line(line):
                    continue
                parsed_line = CustomHandler.parse_line(line)
                reports.append(parsed_line['path'])
            file.close()
            CustomHandler.get_reports(reports)

    @staticmethod
    def process_report_text(sio):
        word_map = dict()
        with io.TextIOWrapper(io.BufferedReader(sio)) as file:
            for line in file:
                tokens = line.split(' ')
                for token in tokens:
                    token = re.sub('[^A-Za-z]+', '', token)
                    if len(token) < 4 or len(token) > 20:
                        continue
                    if token in word_map:
                        word_map[token] += 1
                    else:
                        word_map[token] = 1

            file.close()
        print(word_map)

    @staticmethod
    def get_reports(reports):
        opts = dict()
        opts['url'] = 'ftp.sec.gov'
        opts['paths'] = reports
        opts['handler'] = CustomHandler.process_report_text
        Ftp(opts).run()

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
        for qtr in range(1, 4+1)
    ]
opts['handler'] = CustomHandler.process_index
Ftp(opts).run()
