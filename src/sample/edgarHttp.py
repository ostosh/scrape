import datetime

from scrape.crawl.http import Http
from scrape.handlers.text import Text

opts = dict()
opts['url'] = 'http://sec.gov'

opts['paths'] = [
        '/Archives/edgar/full-index/'+str(year)+'/QTR'+str(qtr)+'/master.gz'
        for year in range(1993, datetime.date.today().year)
        for qtr in range(1,4+1)
    ]
opts['handler'] = Text.to_stdout
Http(opts).run()

