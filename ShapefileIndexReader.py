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

__author__ = 'Sean Taylor Hutchison'
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'Sean Taylor Hutchison'
__email__ = 'seanthutchison@gmail.com'
__status__ = 'Development'


class ShapefileIndex:

    Records = []

    def __bytes_to_index_records(self,file_bytes):
        file_length = len(file_bytes)
        num_records = int((file_length - 100) / 8)
        for record_counter in range(0,num_records):
            byte_position = 100 + (record_counter * 8)
            offset = int.from_bytes(file_bytes[byte_position:byte_position+4], byteorder='big')
            length = int.from_bytes(file_bytes[byte_position+4:byte_position+8], byteorder='big')
            self.Records.append([offset,length])

    def read(self):
        with open(self.Path, 'rb') as shpindex:
            self.__bytes_to_index_records(shpindex.read())

    def __init__(self, path=None):
        if path and os.path.exists(path) and os.path.splitext(path)[1] == '.shx':
            self.Path = path
        else:
            raise FileNotFoundError