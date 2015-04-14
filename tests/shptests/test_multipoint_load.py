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


class LoadMultipointFile(unittest.TestCase):

    multipoint_file = Shapefile(r"../data/Multipoint.shp")
    multipoint_file.read()

    filecode = 9994
    version = 1000
    minimum_file_length = 50
    number_of_records = 3

    def test_NumberOfRecords(self):
        self.assertEqual(len(self.multipoint_file.Records), self.number_of_records)

    def test_ShapeTypeIsMultipoint(self):
        self.assertEqual(self.multipoint_file.Shapetype, Shapefile.Shape.MultiPoint)

    def test_MainHeaderRecord(self):
        self.assertEqual(self.multipoint_file.Header['filecode'], self.filecode)
        self.assertEqual(self.multipoint_file.Header['version'], self.version)
        self.assertGreater(self.multipoint_file.Header['length'], self.minimum_file_length)


if __name__ == '__main__':
    unittest.main()
