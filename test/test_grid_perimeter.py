"""
Unittests for grid perimeter calculations
"""
import os
import numpy as np
import unittest
from grid_perimeter import MpasGrid


class TestGridPerimeter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass 

    def setUp(self):
        self.grid_file = "Manitowoc.static.nc"
        self.mpas_grid = MpasGrid()

    def test_install_setup(self):
        """ Test the installation and unittest setup.  Should always pass."""
        self.assertTrue(True)

    def test_mpas_grid(self):
        """Test the MpasGrid class"""
        self.assertTrue(isinstance(self.mpas_grid, MpasGrid))

    def test_mpas_dataset_dimensions(self):
        """Test read MPAS Grid dataset"""
        self.assertTrue(os.path.exists(self.grid_file))
        mpg = MpasGrid(self.grid_file)
        self.assertEqual(mpg.ncells, 441)
        self.assertEqual(mpg.nvertices, 957)
        self.assertEqual(mpg.nedges, 1397)
        self.assertEqual(mpg.mpas_interior_cell(0), 0)
        
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()
