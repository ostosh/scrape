import os
import tarfile

from ..utils.time import TimeUtils


class Tar:
    @staticmethod
    def to_tar(sio):
        tar = tarfile.open(fileobj=sio)
        out = tarfile.open(os.getcwd() + '/reports/' + str(TimeUtils.unix_time_mills()) + '.tar.gz', mode='w:bz2')
        for file in tar.getmembers():
             out.addfile(file, tar.extractfile(file.name))
        tar.close()
        out.close()

    @staticmethod
    def to_file(sio):
        tar = tarfile.open(fileobj=sio)

        tar.extractall('./reports/')
        tar.close()