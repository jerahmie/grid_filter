"""Unittests with 2D KD tree on MPAS regional data."""
import os
import unittest
from random import uniform
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List
from grid_filter import MPASGrid, KDTree2D
import grid_filter as gf

def dist2d(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Calculate the 2D distance between two points"""
    return sqrt((p2[0] - p1[0])**2 + (p2[1]-p1[1])**2)

def nearest_bf(pt: Tuple[float, float], grid_pts: List[Tuple[float, float, int]]) -> Tuple[float, float, int]:
    """Brute force calculation of nearest point in grid"""

    def dist2d_pt(grid_pt): 
        """closure function with point"""
        return dist2d(pt, grid_pt)

    dist2 = list(map(dist2d_pt, grid_pts))
    dist2_index = dist2.index(min(dist2))
    return grid_pts[dist2_index]

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
#        self.xmin = 1.5
#        self.xmax = 1.0
#        self.ymin = 3.7
#        self.ymax = 5.7
        self.xmin = 0.67
        self.xmax = 0.75
        self.ymin = 4.65
        self.ymax = 4.75
        self.kd2 = KDTree2D(self.ptsi)


    def test_self(self):
        """This should always pass"""
        self.assertTrue(True)
        self.assertEqual(len(self.ptsi), 441)

    def test_internal_pts(self):
        """Test an internal points and make sure next nearest point from 
        KDTree search agrees with brute force search.
        """
        kd2 = KDTree2D(self.ptsi)
        qpts = [(0.75, 4.7), (0.69, 4.8), (0.85, 4.65)]
        for qpt in qpts:
            self.assertEqual(kd2.nearest_cell(qpt), nearest_bf(qpt, self.ptsi)[2])

    def test_random_trees(self):
        """Create a large number of random points near the region of interest
            and performa brute force comparison"""
        npts = 10001
        qpts = [(uniform(self.xmin, self.xmax),
                 uniform(self.ymin, self.ymax)) for i in range(npts)]
        for indx, qpt in enumerate(qpts):
            cell_kd2 = self.kd2.nearest_cell(qpt)
            cell_bf = nearest_bf(qpt, self.ptsi)[2]
            if cell_kd2 != cell_bf:
                print('----> ', qpt)
                cell_lat = np.array([self.ptsi[i][0] for i in range(len(self.ptsi))], dtype=float)
                cell_lon = np.array([self.ptsi[i][1] for i in range(len(self.ptsi))], dtype=float)
                ax = gf.plot_mpas_grid(cell_lat, cell_lon)
                gf.overplot_mpas_grid(ax, np.array([qpt[0]]), np.array([qpt[1]]))
                gf.overplot_mpas_grid(ax, np.array([self.ptsi[cell_kd2][0]]), 
                                      np.array([self.ptsi[cell_kd2][1]]), color='blue')
                gf.overplot_mpas_grid(ax, np.array([self.ptsi[cell_bf][0]]), 
                                      np.array([self.ptsi[cell_bf][1]]), color='magenta')

                plt.savefig('failed_query.png')
            self.assertEqual(cell_kd2, cell_bf)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestKDTree2DStats)
    #unittest.TextTestRunner(resultclass=TestKDTree2DStats.TestResult).run(suite)
