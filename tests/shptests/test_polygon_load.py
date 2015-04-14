"""

"""

__author__ = 'Sean Taylor Hutchison'
__license__ = 'MIT'
__version__ = '0.0.1'
__maintainer__ = 'Sean Taylor Hutchison'
__email__ = 'seanthutchison@gmail.com'
__status__ = 'Development'

import unittest
from ShapefileReader import Shapefile


class LoadPolygonFile(unittest.TestCase):

    polygon_file = Shapefile(r"../data/Polygon.shp")
    polygon_file.read()

    filecode = 9994
    version = 1000
    minimum_file_length = 50
    number_of_records = 4

    def test_NumberOfRecords(self):
        self.assertEqual(len(self.polygon_file.Records), self.number_of_records)

    def test_ShapeTypeIsMultipoint(self):
        self.assertEqual(self.polygon_file.Shapetype, Shapefile.Shape.Polygon)

    def test_MainHeaderRecord(self):
        self.assertEqual(self.polygon_file.Header['filecode'], self.filecode)
        self.assertEqual(self.polygon_file.Header['version'], self.version)
        self.assertGreater(self.polygon_file.Header['length'], self.minimum_file_length)


if __name__ == '__main__':
    unittest.main()