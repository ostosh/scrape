# scrape

scrape started as a library for downloading public reports from the EDGAR FTP server. the current goal for this project is to expand it into a protocol/content agnostic scraper. 

note: repo is WIP


examples:

1. edgarFTP: simple single threaded FTP example to pull all company filings from 1993 - 2015 and dump a
    word count summary for each report to stdout

2. edgarFTPMultiThread: multi-threaded FTP example to pull all company filings from 1993 and dump a
    word count summary for all reports to stdout

3. edgarHTTP: simple single threaded HTTP example to pull all filing index reports from 1993 - 2015 and dump to stdout