import re
from multiprocessing import Pool

import loader
from scrape.crawl.ftp import Ftp
from scrape.handlers.tar import Tar


def get_report(url):
    opts = dict()
    opts['url'] = 'ftp.sec.gov'
    opts['handler'] = Tar.to_file
    opts['paths'] = [url]
    return Ftp(opts).run()


def get_listings():
    opts = dict()
    opts['url'] = 'ftp.sec.gov'
    opts['paths'] = ['/edgar/Feed/2015/QTR3']
    reports = Ftp(opts).list()

    listings = []
    for report in reports:
        if re.match(r'.*\.gz', report) is None:
            continue
        listings.append(report)
    return listings


pool = Pool(20)
pool.map(get_report, get_listings())
