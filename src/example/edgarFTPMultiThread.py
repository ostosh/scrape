import io
import gzip
import re
import operator
from multiprocessing import Pool

from scrape.crawl.ftp import Ftp

word_map = dict()  # hold word count tally


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
        print_top_words()

    @staticmethod
    def process_report_text(sio):
        with io.TextIOWrapper(io.BufferedReader(sio)) as file:
            for line in file:
                tokens = line.split(' ')
                for token in tokens:
                    token = re.sub('[^A-Za-z]+', '', token)
                    if len(token) < 4 or len(token) > 20:
                        continue
                    token = token.lower()
                    if token in word_map:
                        word_map[token] += 1
                    else:
                        word_map[token] = 1

            file.close()

    @staticmethod
    def get_reports(reports):
        opts = dict()
        opts['url'] = 'ftp.sec.gov'
        opts['paths'] = reports
        opts['handler'] = CustomHandler.process_report_text
        Ftp(opts).run()

    @staticmethod
    def is_report_line(line):
        if not line.__contains__("|edgar/data"):
            return False
        if not line.__contains__("10-Q"):
            return False
        else:
            return True

    @staticmethod
    def parse_line(line):
        split = line.split('|')
        parsed = dict()
        parsed['cik'] = split[0]
        parsed['reportType'] = split[2]
        parsed['fileDate'] = split[3]
        parsed['path'] = split[4].strip('\n')
        return parsed


def get_report(url):
    opts = dict()
    opts['url'] = 'ftp.sec.gov'
    opts['handler'] = CustomHandler.process_index
    opts['paths'] = [url]
    return Ftp(opts).run()


def print_top_words():
    sorted_map = sorted(word_map.items(), key=operator.itemgetter(1), reverse=True)
    count = len(sorted_map)
    [print(sorted_map[i], end='') for i in range(min(count, 10))]
    if count > 1:
        print()

paths = [
    '/edgar/full-index/'+str(year)+'/QTR'+str(qtr)+'/master.gz'
    for year in range(1993, 2000)  # this should keep us busy for a while...
    for qtr in range(1, 4+1)
]

pool = Pool(15)
pool.map(get_report, paths)
