import urllib.request
import time 
import types

from ..handlers.text import Text
from ..utils.io import BufferedReader
from ..utils.time import TimeUtils


class HTTPError(Exception):
    pass


class IllegalArgumentException(Exception):
    pass


class Http:
    def __init_props__(self, props):
        if type(props) is not dict:
            raise IllegalArgumentException('Error: invalid props object given.')
        if 'url' not in props or type(props['url']) is not str:
            raise IllegalArgumentException('Error: invalid domain arg of props.')
        if 'paths' not in props or type(props['paths']) is not list:#TODO add type check for list elems
            raise IllegalArgumentException('Error: invalid paths arg of props')
        if 'timeout' not in props or type(props['timeout']) is not int:
            props['timeout'] = 99999999
        if 'chunksize' not in props or type(props['chunksize']) is not int:
            props['chunksize'] = 80 
        if 'filehandler' not in props or type(props['filehandler']) is not types.FunctionType:
            props['filehandler'] = Text.to_stdout
        self.props = props

    def __init_conn__(self): # TODO add validation for bad path
        self.http = urllib.request

    def __init__(self, props):
        self.__init_props__(props)
        self.__init_conn__()
     
    def run(self):
        for path in self.props['paths']:
            while True:
                try:
                    self.get_report(path)
                    time.sleep(0.1)
                    break
                except Exception as e: # TODO add validation for bad path
                    print('Error: HTTP failure while downloading. Reseting Connection: {0}. '.format(e))
                    continue

    def get_report(self, uri):
        reader = BufferedReader()
        resp = self.http.urlopen(self.props['url'], timeout = self.props['timeout'])
        print('[{0}] GETTING: {1} '.format(TimeUtils.unix_time_mills(), uri))
        
        while True:
            try:
                data = resp.read(self.props['chunksize'])
                if not data:
                    break
                reader.buffer_data(data)
            except Exception as e:
                raise HTTPError(e, uri)
        reader.save_file(self.dump_report)

    def dump_report(self, sio):
        self.props['filehandler'](sio)
