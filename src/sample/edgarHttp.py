from scrape.crawl.http import Http
from scrape.handlers.text import Text

opts = {}
opts['url'] = 'http://sec.gov'
opts['paths'] = ['/Archives/edgar/full-index/1993/QTR1/master.gz',
                 '/Arhicves/edgar/full-index/1994/QTR1/master.gz',
                 '/Arhicves/edgar/full-index/1995/QTR1/master.gz']
opts['filehandler'] = Text.to_txt
trans = Http(opts)
trans.run()
