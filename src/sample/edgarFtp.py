from scrape.crawl.ftp import Ftp
from scrape.handlers.gzip import Gzip

opts = {}
opts['url'] = 'ftp.sec.gov'
opts['paths'] = ['/edgar/full-index/1993/QTR1/master.gz',
                 '/edgar/full-index/1994/QTR1/master.gz',
                 '/edgar/full-index/1995/QTR1/master.gz']
opts['filehandler'] = Gzip.to_txt
trans = Ftp(opts)
trans.run()
