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

    def __init__(self, path=None):
        if path and os.path.exists(path) and os.path.splitext(path)[1] == '.dbf':
            self.Path = path
        else:
            raise FileNotFoundError