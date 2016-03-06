import sys
import os
sys.path.insert(0, os.path.abspath('..'))

import unittest
import io
import glob

from scrape.handlers.text import Text


class TestTextHandlers(unittest.TestCase):
    def test_to_stdout(self):
        test_file = open('test.txt', 'w+')
        sys.stdout = test_file
        sio = io.BytesIO()
        sio.write(b"TEST")
        sio.seek(0)
        Text.to_stdout(sio)
        test_file.seek(0)
        line = test_file.read()
        test_file.close()
        os.remove('test.txt')
        self.assertEqual('TEST', line)

    def test_to_text(self):
        sio = io.BytesIO()
        sio.write(b"TEST")
        sio.seek(0)
        Text.to_txt(sio)
        test_file_name = glob.glob("*.txt")[0]
        test_file = open(test_file_name, 'r')
        line = test_file.read()
        test_file.close()
        os.remove(test_file_name)
        self.assertEqual('TEST', line)

