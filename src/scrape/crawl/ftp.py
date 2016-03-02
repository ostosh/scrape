from ftplib import FTP, error_reply, error_temp, error_proto
from copy import deepcopy
import re
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
            props['paths'] = ['/']
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
        while True:
            try:
                self.ftp = FTP(self.props['url'], '', '', self.props['timeout'])
                self.ftp.login()
                return
            except (EOFError) as e:
                LogUtils.log_error('temp FTP failure while retrieving {0}. Resetting'.format(e))
                time.sleep(2)
                continue

    def __init__(self, props):
        self.__init_props__(props)
    
    def __close_conn__(self):
        self.ftp.close()

    def run(self):
        self.__init_conn__()
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
                except (error_reply, error_temp, error_proto, EOFError) as e:
                    self.__init_conn__()
                    LogUtils.log_error('temp FTP failure while retrieving {0}. Resetting {1}'.format(path, e))
                    continue
                except Exception as e:
                    LogUtils.log_error('perm FTP failure while retrieving {0}. Skipping {1}'.format(path,  e))
                    break
        self.__close_conn__()

    def list(self):
        self.__init_conn__()
        to_vist = deepcopy(self.props['paths'])
        while len(to_vist) > 0:
            current = to_vist.pop(0)
            paths = self.ftp.nlst(current)
            for path in paths:
                if re.match(r'.*\..*', path) is None:
                    to_vist.append(path)
                else:
                    yield path

        self.__close_conn__()


    def get_contents(self, path):
        return self.ftp.nlst(path)

    def retrieve(self, uri):
        reader = BufferedReader()
        LogUtils.log_info('ftp retrieving {0}'.format(uri))
        self.ftp.retrbinary('RETR ' + uri, callback=reader.buffer_data, blocksize=102400)
        reader.save_file(self.dump_report)

    def dump_report(self, sio):
        self.props['handler'](sio)
