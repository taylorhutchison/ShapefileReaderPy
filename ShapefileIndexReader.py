"""
This script exposes a class used to read the Shapefile Index format
used in conjunction with a shapefile. The Index file gives the record
number and content length for every record stored in the main shapefile.
This is useful if you need to extract specific features from a shapefile
without reading the entire file.

How to use:
    from ShapefileIndexReader import ShapefileIndex
    shx = ShapefileIndex(Path/To/index.shx)
    shx.read()

The 'shx' object will expose three properties
    1) Path - the path given to the shapefile, if it exists
    2) Offsets - an array of byte offsets for each record in the main shapefile
    3) Lengths - an array of 16-bit word lengths for each record in the main shapefile
"""

import os
import struct

__author__ = 'Sean Taylor Hutchison'
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'Sean Taylor Hutchison'
__email__ = 'seanthutchison@gmail.com'
__status__ = 'Development'


class ShapefileIndex:

    def __init__(self, path=None):
        if path and os.path.exists(path) and os.path.splitext(path)[1] == '.shx':
            self.Path = path
        else:
            raise FileNotFoundError