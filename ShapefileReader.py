"""
This script exposes a class used to read the shapefile format.
It is read according to the standard published by
ESRI at http://www.esri.com/library/whitepapers/pdfs/shapefile.pdf.
The class is Shapefile, which when instantiated is pointed to the
path of a .shp file.

How to use:
    from ShapefileReader import Shapefile
    shp = Shapefile(Path/To/shapefile.shp)
    shp.read()

The 'shp' object will have four public properties exposed:
    1) Path - the path given to the shapefile, if it exists
    2) Header - the main file header contains meta information about shape type, file length, and bounding geometry
    3) Records - an array of records, nested according to the shape type.
    4) Shapetype - an Enum for the shape type (e.g. Point, Polyline, Polygon, etc.)
"""

import os
import struct
from enum import Enum

__author__ = 'Sean Taylor Hutchison'
__license__ = 'MIT'
__version__ = '0.0.1'
__maintainer__ = 'Sean Taylor Hutchison'
__email__ = 'seanthutchison@gmail.com'
__status__ = 'Development'


class Shapefile:

    # The full path to the shapefile
    Path = None
    # The Shapefile main header info
    Header = {}
    # A nested array of point values
    Records = []
    # The shapefile type (i.e. point, polyline, etc.) as a ShapeType Enum
    Shapetype = None

    # A shapefile has a single shape type defined as an integer from bytes 32 thru 36 in the main file header.
    # The integer corresponds to pre-defined shape types. This Enum makes dealing with the shape type easier by
    # not having to deal directly with the integer representation.
    class Shape(Enum):
        Null = 0
        Point = 1
        Polyline = 3
        Polygon = 5
        MultiPoint = 8
        PointZ = 11
        PolylineZ = 13
        PolygonZ = 15
        MultiPointZ = 18
        PointM = 21
        PolylineM = 23
        PolygonM = 25
        MultiPointM = 28
        MultiPatch = 31

    # This method takes all the main record bytes and transforms them into an array of x, y pairs.
    # An example resulting structure is [ [x,y], [x,y], [x,y] ], which represents three distinct point features.
    @staticmethod
    def __bytes_to_point_records(file_bytes):
        point_records = []
        byte_position = 0
        while byte_position < len(file_bytes):
            px = struct.unpack("<d", file_bytes[byte_position+12:byte_position+20])[0]
            py = struct.unpack("<d", file_bytes[byte_position+20:byte_position+28])[0]
            point_records.append([px, py])
            byte_position += 28
        return point_records

    # This method takes all the main record bytes and transforms them into an array of multipoint sets.
    # An example resulting structure is [ [ [x,y], [x,y], [x,y] ], [ [x,y], [x,y] ] ], which represents two
    # distinct features, the first feature has three points, and the second feature has two points.
    @staticmethod
    def __bytes_to_multipoint_records(file_bytes):
        multipoint_records = []
        byte_position = 0
        while byte_position < len(file_bytes):
            multipoint = []
            num_points = int.from_bytes(file_bytes[byte_position+44:byte_position+48], byteorder='little')
            for point_counter in range(0, num_points):
                point_position = byte_position + (point_counter*16+48)
                px = struct.unpack("<d", file_bytes[point_position:point_position+8])[0]
                py = struct.unpack("<d", file_bytes[point_position+8:point_position+16])[0]
                multipoint.append([px, py])
            multipoint_records.append(multipoint)
            byte_position += (48 + (16 * num_points))
        return multipoint_records

    # This method takes all the main record bytes and transforms them into an array of "polytype" sets.
    # Polygons are nearly identical to Polylines, except that they are "closed" meaning the final point
    # in the series of points for each feature is identical to the starting point. It is possible to
    # create both Polyline and Polygon types using the same method, because their structure is so similar.
    # Polylines and Polygons can have multiple parts per features, and therefore all the points in a feature
    # may not be connected.
    # An example resulting structure is [ [ [ [x,y], [x,y], [x,y] ], [ [x,y], [x,y] ] ] ], which represents a
    # single polyline feature with two parts. The first part has three connected points, and the second part has
    # two connected points.
    @staticmethod
    def __bytes_to_polytype_records(file_bytes):
        polyline_records = []
        byte_position = 0
        while byte_position < len(file_bytes):
            polyline = []
            part_index = []
            points = []
            num_parts = int.from_bytes(file_bytes[byte_position+44:byte_position+48], byteorder='little')
            num_points = int.from_bytes(file_bytes[byte_position+48:byte_position+52], byteorder='little')
            for part_counter in range(0, num_parts):
                part_byte_start = byte_position+(part_counter*4)+52
                part_start_index = int.from_bytes(file_bytes[part_byte_start:part_byte_start+4], byteorder='little')
                part_index.append(part_start_index)
            for point_counter in range(0, num_points):
                point_position = byte_position+(point_counter*16+(4 * num_parts) + 52)
                px = struct.unpack("<d", file_bytes[point_position:point_position+8])[0]
                py = struct.unpack("<d", file_bytes[point_position+8:point_position+16])[0]
                points.append([px, py])
            if len(part_index) == 1:
                polyline.append(points)
            else:
                part_index.append(len(points)-1)
                for part_start in range(0, len(part_index)-1):
                    polyline.append(points[part_index[part_start]:part_index[part_start+1]])
            polyline_records.append(polyline)
            byte_position += 52 + (4 * num_parts) + (num_points * 16)
        return polyline_records

    # The first 100 bytes of a .shp file contains the "main file header". Which is essentially some
    # metadata about the shape type, file length, and bounding information. There is also information
    # about the version and filecode, which are always 1000 and 9994 respectively.
    # The first 28 bytes of the header are in big endian notation, and the rest are in little endian.
    # For more information consult the specification at http://www.esri.com/library/whitepapers/pdfs/shapefile.pdf
    def __bytes_to_header(self, file_bytes):
        self.Header['filecode'] = int.from_bytes(file_bytes[0:4], byteorder='big')
        self.Header['length'] = int.from_bytes(file_bytes[24:28], byteorder='big')
        self.Header['version'] = int.from_bytes(file_bytes[28:32], byteorder='little')
        self.Header['type'] = int.from_bytes(file_bytes[32:36], byteorder='little')
        self.Header['xmin'] = struct.unpack("<d", file_bytes[36:44])[0]
        self.Header['ymin'] = struct.unpack("<d", file_bytes[44:52])[0]
        self.Header['xmax'] = struct.unpack("<d", file_bytes[52:60])[0]
        self.Header['ymax'] = struct.unpack("<d", file_bytes[60:68])[0]
        self.Header['zmin'] = struct.unpack("<d", file_bytes[68:76])[0]
        self.Header['zmax'] = struct.unpack("<d", file_bytes[76:84])[0]
        self.Header['mmin'] = struct.unpack("<d", file_bytes[84:92])[0]
        self.Header['mmax'] = struct.unpack("<d", file_bytes[92:100])[0]
        self.Shapetype = Shapefile.Shape(self.Header['type'])

    # A wrapper method that takes the shape type and calls the appropriate method.
    def __bytes_to_records(self, file_bytes):
        if self.Shapetype == Shapefile.Shape.Null:
            self.Records = [None] * (file_bytes / 4)
        elif self.Shapetype == Shapefile.Shape.Point:
            self.Records = Shapefile.__bytes_to_point_records(file_bytes)
        elif self.Shapetype == Shapefile.Shape.MultiPoint:
            self.Records = Shapefile.__bytes_to_multipoint_records(file_bytes)
        elif self.Shapetype == Shapefile.Shape.Polyline or self.Shapetype == Shapefile.Shape.Polygon:
            self.Records = Shapefile.__bytes_to_polytype_records(file_bytes)

    # The only publicly exposed method of the class. This reads the shapefile and stores the main header and
    # record information in the Header and Records properties respectively.
    def read(self):
        with open(self.Path, 'rb') as shpfile:
            self.__bytes_to_header(shpfile.read(100))
            file_length_in_bytes = self.Header['length'] * 2 - 100
            self.__bytes_to_records(shpfile.read(file_length_in_bytes))

    def __init__(self, path=None):
        if path and os.path.exists(path) and os.path.splitext(path)[1] == '.shp':
            self.Path = path
        else:
            raise FileNotFoundError