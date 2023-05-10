"""Unittests with 2D KD tree on MPAS regional data."""
import os
import unittest
from random import uniform
from grid_perimeter import MPASGrid, KDTree2D

class TestKDTree2DStats(unittest.TestCase):
    """Test cases for compiling statistics about KD Tree."""
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        this_dir = os.path.abspath(os.path.dirname(__file__)) # test/ directory
        self.grid_file = os.path.join(this_dir, 'Manitowoc.static.nc')
        self.mpg = MPASGrid(self.grid_file)
        pts = self.mpg.cell_points()
        self.ptsi = [(pts[i][0], pts[i][1], i) for i in range(len(pts))]

    def test_self(self):
        """This should always pass"""
        self.assertTrue(True)
        self.assertEqual(len(self.ptsi), 441)


    def test_internal_pts(self):
        """Test an internal points and make sure next nearest point from 
        KDTree search agrees with brute force search.
        """
        qpt = (0.75, 4.7)
        kd2 = KDTree2D(self.ptsi)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()