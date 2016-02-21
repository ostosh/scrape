from ftplib import FTP, error_reply, error_temp, error_proto

import time 
import types

from ..handlers.gzip import Gzip
from ..utils.io import BufferedReader
from ..utils.log import LogUtils


class IllegalArgumentException(Exception):
    pass


class Ftp:
    def __init_props__(self, props):
        if type(props) is not dict:
            raise IllegalArgumentException('Error: invalid props object given.')
        if 'url' not in props or type(props['url']) is not str:
            raise IllegalArgumentException('Error: invalid domain arg of props.')
        if 'paths' not in props or type(props['paths']) is not list:
            raise IllegalArgumentException('Error: invalid paths arg of props')
        if 'maxAttempts' not in props or type(props['timeout']) is not int:
            props['maxAttempts'] = 5
        if 'timeout' not in props or type(props['timeout']) is not int:
            props['timeout'] = 99999999
        if 'delay' not in props or type(props['timeout']) is not float:
            props['delay'] = 0.005
        if 'handler' not in props or type(props['handler']) is not types.FunctionType:
            props['handler'] = Gzip.to_stdout
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
            attempts = 0
            while True:
                attempts += 1
                if attempts > self.props['maxAttempts']:
                    LogUtils.log_error('perm HTTP failure max attempts exceeded while retrieving {0}'.format(path))
                    break
                try:
                    self.retrieve(path)
                    time.sleep(self.props['delay'])
                    break
                except (error_reply, error_temp, error_proto) as e:
                    LogUtils.log_error('temp FTP failure while retrieving {0}. Resetting {1}'.format(path, e))
                    self.__reset_conn__()
                    continue
                except Exception as e:
                    LogUtils.log_error('perm FTP failure while retrieving {0}. Skipping {1}'.format(path,  e))
                    break

    def retrieve(self, uri):
        reader = BufferedReader()
        LogUtils.log_info('ftp retrieving {0}'.format(uri))
        self.ftp.sendcmd('TYPE i')
        report_size = self.ftp.size(uri)
        self.ftp.sendcmd('TYPE a')

        while reader.get_buffered_size() < report_size:
            self.ftp.retrbinary('RETR ' + uri, callback=reader.buffer_data)
        reader.save_file(self.dump_report)

    def dump_report(self, sio):
        self.props['handler'](sio)
