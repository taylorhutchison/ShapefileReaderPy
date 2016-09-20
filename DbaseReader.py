"""
This script exposes a class used to read the dbase format
used in conjunction with a shapefile. There are several types
of dbase formats, but the one that is used with shapefiles is
version 5.

How to use:
    from DbaseReader import Dbase
    dbf = Dbase(Path/To/dbasefile.dbf)
    dbf.read()

The 'dbf' object will expose a two properties and one method
    1) Path - the path given to the shapefile, if it exists
    2) Table - A dictionary of arrays containing the data.
    3) GetRecord(id) - Returns an array of data for a given id
"""

import os
import struct

__author__ = 'Sean Taylor Hutchison'
__license__ = 'MIT'
__version__ = '0.0.1'
__maintainer__ = 'Sean Taylor Hutchison'
__email__ = 'seanthutchison@gmail.com'
__status__ = 'Development'


class Dbase:

    Path = None

    def read(self):
         with open(self.Path, 'rb') as dbasefile:
             file_bytes = dbasefile.read(800)
             version = int.from_bytes(file_bytes[0:1], byteorder='big')
             dbase_version = int(str((version >> 0) & 1) + str((version >> 1) & 1),2)
             year = (int.from_bytes(file_bytes[1:2], byteorder='little'))
             month = (int.from_bytes(file_bytes[2:3], byteorder='little'))
             day = (int.from_bytes(file_bytes[3:4], byteorder='little'))
             record_count = int.from_bytes(file_bytes[4:8], byteorder='little')
             header_bytes = int.from_bytes(file_bytes[8:10], byteorder='little')
             record_bytes = int.from_bytes(file_bytes[10:12], byteorder='little')
             for i in range(0,20):
                jump = 32
                start = 30 + (jump * i)
                first_record = file_bytes[start:(start+jump)]
                name = ''
                for b in first_record[0:11]:
                    name = name + chr(b)
                print(name)


    def __init__(self, path=None):
        if path and os.path.exists(path) and os.path.splitext(path)[1] == '.dbf':
            self.Path = path
        else:
            raise FileNotFoundError