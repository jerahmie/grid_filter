"""Unittests with 2D KD tree on MPAS regional data."""
import os
import unittest
from grid_filter import MPASGrid, KDTree2D, KDTreeDisplay

class TestKDTreeDisplay(unittest.TestCase):
    """Test cases for compiling statistics about KD Tree Display"""
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        this_dir = os.path.abspath(os.path.dirname(__file__)) # test/ directory
        self.grid_file = os.path.join(this_dir, 'Manitowoc.static.nc')
        self.mpg = MPASGrid(self.grid_file)
        pts = self.mpg.cell_points()
        self.ptsi = [(pts[i][0], pts[i][1], i) for i in range(len(pts))]
        self.kd2 = KDTree2D(self.ptsi)

    def test_self(self):
        """This should always pass"""
        self.assertTrue(True)
        self.assertEqual(len(self.ptsi), 441)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
