"""
Unittests for grid perimeter calculations
"""
import os
import numpy as np
import unittest
from grid_filter import MPASGrid, len_non_zero, border_cell_ids_from_cells_per_vertices

class TestGridPerimeter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass 

    def setUp(self):
        this_dir = os.path.abspath(os.path.dirname(__file__))
        self.grid_file = os.path.join(this_dir, "Manitowoc.static.nc")
        self.mpas_grid = MPASGrid()

    def test_install_setup(self):
        """ Test the installation and unittest setup.  Should always pass."""
        self.assertTrue(True)

    def test_mpas_grid(self):
        """Test the0 MpasGrid class"""
        self.assertTrue(isinstance(self.mpas_grid, MPASGrid))

    def test_len_non_zero(self):
        """Test len_non_zero.  Should return the number of non-zero elements in array."""
        a = [125, 254, 612, 0, 0, 0, 0, 0, 0, 0]
        a_len = 10          # total number of values in a
        a_non_zero_len = 3  # number of non-zero values in a
        self.assertEqual(len(a), a_len)
        self.assertEqual(len_non_zero(a), a_non_zero_len)
        self.assertEqual(len_non_zero([0, 0, 0, 0]), 0)
        self.assertEqual(len_non_zero([0, 1, 0]), 1)
        self.assertEqual(len_non_zero([1, 2, 3, 4, 5]), 5)

    def test_id_borders(self):
        """Test the id_borders function"""
        a = [1.0, 0.5, 0.6, 1.0]
        a_border = [1, 2]
        b = [(0,1.0), (1,0.5), (2,0.6), (3,1.0)]
        self.assertEqual(border_cell_ids_from_cells_per_vertices(a), a_border)

    def test_mpas_dataset_dimensions(self):
        """Test read MPAS Grid dataset"""
        self.assertTrue(os.path.exists(self.grid_file))
        mpg = MPASGrid(self.grid_file)
        self.assertEqual(mpg.ncells, 441)
        self.assertEqual(mpg.nvertices, 957)
        self.assertEqual(mpg.nedges, 1397)
 
    def test_border_cell_helper(self):
        """Test the ratio of edges per vertices of cells"""
        a_grid = [1.0, 0.5, 1.0, 1.0, 1.0, 0.7, 1.0, 1.0, 1.0, 0.7,
                  1.0, 1.0, 1.0, 0.7, 0.7, 1.0, 1.0, 0.7, 1.0, 0.7, 
                  1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0,
                  1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.7, 1.0,
                  0.7, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 
                  1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.7, 1.0, 1.0,
                  0.5, 0.7, 1.0, 1.0, 1.0, 1.0, 0.7, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.7, 
                  0.7, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 0.7, 0.7, 0.7, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.7,
                  1.0, 0.7, 0.7, 0.7, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 0.7, 0.7, 1.0, 1.0, 0.7, 0.7,
                  1.0, 1.0, 0.7, 1.0, 1.0, 0.7, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.7, 0.7,
                  1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.7, 1.0, 1.0, 0.8,
                  1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.7,
                  0.7, 1.0, 0.7, 0.7, 1.0]
        a_border = [1, 5, 9, 13, 14, 17, 19, 26, 31, 38, 40, 57,
                    60, 61, 66, 79, 80, 91, 92, 93, 112, 119, 121,
                    122, 123, 134, 135, 138, 139, 142, 145, 158, 159,
                    166, 169, 189, 190, 192, 193]
        self.assertEqual(border_cell_ids_from_cells_per_vertices(a_grid), a_border)

    def test_egde_cells(self):
        """Test edge cell calculations
        """
        mpg = MPASGrid(self.grid_file)
        border_cells = mpg.border_cell_ids
        self.assertEqual(len(border_cells), 71)
    

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()
