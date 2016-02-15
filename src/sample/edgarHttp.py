import datetime

from scrape.crawl.http import Http
from scrape.handlers.text import Text

opts = {}
opts['url'] = 'http://sec.gov'

opts['paths'] = [
        '/Archives/edgar/full-index/'+str(year)+'/QTR'+str(qtr)+'/master.gz'
        for year in range(1993, datetime.date.today().year)
        for qtr in range(1,4+1)
    ]
opts['filehandler'] = Text.to_txt
trans = Http(opts)
trans.run()
