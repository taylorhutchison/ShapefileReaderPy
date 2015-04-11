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


class LoadPointFile(unittest.TestCase):

    point_file = Shapefile(r"data/Point.shp")
    point_file.read()

    def test_NumberOfRecords(self):
        self.assertEqual(len(self.point_file.Records), 26)

    def test_ShapeTypeIsPoint(self):
        self.assertEqual(self.point_file.Shapetype, Shapefile.Shape.Point)

    def test_MainHeaderRecord(self):
        self.assertEqual(self.point_file.Header['filecode'], 9994)
        self.assertEqual(self.point_file.Header['version'], 1000)
        self.assertGreater(self.point_file.Header['length'], 50)

if __name__ == '__main__':
    unittest.main()
