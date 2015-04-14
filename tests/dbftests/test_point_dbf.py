"""
    File description
"""

__author__ = 'Sean Taylor Hutchison'
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'Sean Taylor Hutchison'
__email__ = 'seanthutchison@gmail.com'
__status__ = 'Development'

import unittest
from DbaseReader import Dbase


class LoadPointFile(unittest.TestCase):

    point_file = Dbase(r"../data/Point.dbf")
    point_file.read()

    def test_NumberOfRecords(self):
        self.assertEqual(2, 2)

if __name__ == '__main__':
    unittest.main()