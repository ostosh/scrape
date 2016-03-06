import datetime

import loader
from scrape.crawl.http import Http
from scrape.handlers.gzip import Gzip

opts = dict()
opts['url'] = 'http://sec.gov'

opts['paths'] = [
        '/Archives/edgar/full-index/'+str(year)+'/QTR'+str(qtr)+'/master.gz'
        for year in range(1993, datetime.date.today().year)
        for qtr in range(1, 4+1)
    ]
opts['handler'] = Gzip.to_stdout
Http(opts).run()
