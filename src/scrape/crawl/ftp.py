from ftplib import FTP

import time 
import types

from ..handlers.gzip import Gzip
from ..utils.io import BufferedReader
from ..utils.time import TimeUtils


class FtpError(Exception):
    pass


class IllegalArgumentException(Exception):
    pass


class Ftp:
    def __init_props__(self, props):
        if type(props) is not dict:
            raise IllegalArgumentException('Error: invalid props object given.')
        if 'url' not in props or type(props['url']) is not str:
            raise IllegalArgumentException('Error: invalid domain arg of props.')
        if 'paths' not in props or type(props['paths']) is not list: #TODO add type check for list elems
            raise IllegalArgumentException('Error: invalid paths arg of props')
        if 'timeout' not in props or type(props['timeout']) is not int:
            props['timeout'] = 99999999
        if 'filehandler' not in props or type(props['filehandler']) is not types.FunctionType:
            props['filehandler'] = Gzip.to_stdout
        self.props = props
        
    def __init_conn__(self): # TODO add validation for bad path
        self.ftp = FTP(self.props['url'], '', '', self.props['timeout'])
        self.ftp.login()

    def __init__(self, props):
        self.__init_props__(props)
        self.__init_conn__()
    
    def __close_conn__(self):
        self.ftp.close()

    def __reset_conn__(self):
        self.__close_conn__()
        self.__init_conn__()

    def run(self):
        for path in self.props['paths']:
            while True:
                try:
                    self.get_report(path)
                    time.sleep(0.1)
                    break
                except Exception as e: # TODO add validation for bad path
                    print('Error: FTP failure while downloading. Reseting Connection: {0}. '.format(e))
                    self.__reset_conn__()
                    continue

    def get_report(self, uri):
        reader = BufferedReader()
        self.ftp.sendcmd('TYPE i')
        report_size = self.ftp.size(uri)
        self.ftp.sendcmd('TYPE a')
        print('[{0}] GETTING: {1} '.format(TimeUtils.unix_time_mills(), uri))
        
        while reader.get_buffered_size() < report_size:
                try:
                    self.ftp.retrbinary('RETR ' + uri, callback=reader.buffer_data)
                except Exception as e:
                    raise FtpError(e, uri)
        reader.save_file(self.dump_report)

    def dump_report(self, sio):
        self.props['filehandler'](sio)
