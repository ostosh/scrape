from urllib import request, error
import time 
import types

from ..handlers.text import Text
from ..utils.io import BufferedReader
from ..utils.log import LogUtils


class IllegalArgumentException(Exception):
    pass


class Http:
    def __init_props__(self, props):
        if type(props) is not dict:
            raise IllegalArgumentException('invalid props object given.')
        if 'url' not in props or type(props['url']) is not str:
            raise IllegalArgumentException('invalid domain of props.')
        if 'paths' not in props or type(props['paths']) is not list:
            raise IllegalArgumentException('invalid paths of props')
        if 'maxAttempts' not in props or type(props['maxAttempts']) is not int:
            props['maxAttempts'] = 5
        if 'timeout' not in props or type(props['timeout']) is not int:
            props['timeout'] = 1.0
        if 'delay' not in props or type(props['delay']) is not float:
            props['delay'] = 0.005
        if 'chunksize' not in props or type(props['chunksize']) is not int:
            props['chunksize'] = 80 
        if 'filehandler' not in props or type(props['filehandler']) is not types.FunctionType:
            props['filehandler'] = Text.to_stdout
        self.props = props

    def __init_conn__(self):
        self.http = request

    def __init__(self, props):
        self.__init_props__(props)
        self.__init_conn__()
     
    def run(self):
        for path in self.props['paths']:
            attempts = 0
            while True:
                attempts += 1
                if attempts > self.props['maxAttempts']:
                    LogUtils.log_error('perm HTTP failure retrieving {0}'.format(path))
                    break
                try:
                    self.retrieve(self.props['url'] + path)
                    time.sleep(self.props['delay'])
                    break
                except error.HTTPError as e:
                    if e.code in range(500, 506):
                        LogUtils.log_error('temp HTTP failure {0}: {1}'.format(path, e))
                        continue
                    else:
                        LogUtils.log_error('perm HTTP failure {0}: {1}'.format(path,  e))
                        break
                except Exception as e:
                    LogUtils.log_error('perm HTTP failure {0}: {1}'.format(path,  e))
                    break

    def retrieve(self, url):
        reader = BufferedReader()
        LogUtils.log_info('http retrieving {0} '.format(url))
        resp = self.http.urlopen(url, timeout=self.props['timeout'])
        
        while True:
            data = resp.read(self.props['chunksize'])
            if not data:
                break
            reader.buffer_data(data)
        reader.save_file(self.dump_report)

    def dump_report(self, sio):
        self.props['handler'](sio)
