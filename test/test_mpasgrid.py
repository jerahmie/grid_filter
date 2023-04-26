"""Unit testing for MPASGrid Class"""
import os
import unittest
from grid_perimeter import MPASGrid

class TestMPASGrid(unittest.TestCase):
    """MPASGrid TestCase"""
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        this_directory = os.path.abspath(os.path.dirname(__file__))
        self.data_file = os.path.join(this_directory, "Manitowoc.static.nc")
        self.mpg = MPASGrid(self.data_file)

    def test_unittest_setup(self):
        """Ensure the TestCase class is configured correctly.
        This should always pass.
        """
        self.assertTrue(True)

    def test_MPASGrid_type(self):
        """Ensure the MPASGrid Class can be instantiated with correct type"""
        mpg_empty = MPASGrid()
        self.assertTrue(isinstance(mpg_empty, MPASGrid))
        mpg_test_data = MPASGrid(self.data_file)
        self.assertTrue(isinstance(mpg_test_data, MPASGrid))

    def test_MPASGrid_lat_lon(self):
        """Test the extraction of MPAS grid latitude and longitude data """
        pts = self.mpg.cell_points()
        self.assertEqual(str(type(pts)), '<class \'list\'>')
        self.assertEqual(len(pts), 441)
        self.assertEqual(str(type(pts[0])), '<class \'tuple\'>')
        self.assertEqual(len(pts[0]), 2)
        self.assertEqual(str(type(pts[0][0])), '<class \'float\'>')
        self.assertEqual(str(type(pts[0][1])), '<class \'float\'>')

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
