import datetime
import hashlib
import re

from logger import getgglogger

logger = getgglogger(__name__)
filetype_re_rule = \
    re.compile(r'wind_extreme_\d{4}(0?[1-9]|1[012])(0?[1-9]|[12][0-9]|3[01]).dat')


class DatFile:
    def read_data(self):
        """
        reads data in the file and fills:
        self.data

        with its content.
        :return: True
        """

        file_ob = self.open_file()
        for line in file_ob.readlines():
            if 'aa/mm/gg' not in line:
                datalist = line.split(';')
                try:
                    self.data.append([
                        datetime.datetime.strptime(datalist[0], '%d/%m/%Y %H.%M.%S'),
                        float(datalist[1]),
                        int(datalist[2]),
                        int(datalist[3])
                    ])
                except ValueError:
                    logger.debug(f'line {line} in file {self.filepath} cannot be read')

        logger.debug(f'Done Reading Data File')
        return True

    def open_file(self):
        return open(
                self.filepath, 'r', encoding='latin1')

    def sha256sum(self):
        """
        https://stackoverflow.com/questions/22058048/hashing-a-file-in-python#answer-44873382
        reads the datafile in chunks and returns the hexdigest of the content

        :return: hexdigest of the file content
        """
        h = hashlib.sha256()
        b = bytearray(128 * 1024)
        mv = memoryview(b)
        with open(self.filepath, 'rb', buffering=0) as f:
            for n in iter(lambda: f.readinto(mv), 0):
                h.update(mv[:n])
        logger.debug(f'hex digest computed')
        return h.hexdigest()

    def __init__(self, filepath):
        self.file_header = {}
        self.data_header = []
        self.data = []
        self.filepath = filepath

        # it opens/reads the file twice
        self.hash_digest = self.sha256sum()
        self.read_data()


if __name__ == "__main__":
    import os

    print(DatFile(os.path.join('log_folder/wind_extreme_20211028.dat')).data)