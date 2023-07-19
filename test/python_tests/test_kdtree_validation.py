'''Unittests for kdtree module validation.
'''
import os
import unittest
import grid_filter as gf
import h5py
import netCDF4
import numpy as np

class TestKDTreeValidation(unittest.TestCase):
    '''Validation of KDTree filtering'''
    @classmethod
    def setUpClass(cls):
        this_dir = os.path.abspath(os.path.dirname(__file__))
        cls.obs_file = os.path.join(this_dir,'satwind_obs_2019050100.h5')
        cls.static_file = os.path.join(this_dir,'Manitowoc.static.nc')
        mpg = gf.MPASGrid(cls.static_file)
        cls.bdy_msk = mpg.bdy_mask_cells
        cls.pts = mpg.cell_points()
        cls.obs_pts = gf.obs_points(cls.obs_file)

    def setUp(self):
        pass

    def test_TestKDTreeValidation(self):
        '''Test that the TestDKTreeValidation class is setup correctly.'''
        self.assertTrue(True)
        self.assertTrue(os.path.exists(self.obs_file))
        self.assertTrue(os.path.exists(self.static_file))

    #@unittest.skip("Long test")
    def test_bdy_msk_types(self):
        '''Test full kdtree'''
        ptsi = [(180.0/np.pi*self.pts[i][0], 180.0/np.pi*self.pts[i][1], i) for i in range(len(self.pts))]
        self.assertEqual(len(ptsi), 441)
        kd2d_full = gf.KDTree2D(ptsi)

        ptsi_filtered, _ = gf.filter_bdy_mask_cell(ptsi, self.bdy_msk, {6,7})
        print(f'len(self.bdy_msk) {len(self.bdy_msk)}')
        self.assertEqual(len(ptsi_filtered), 136)
        kd2d_filtered = gf.KDTree2D(ptsi_filtered)
        mask_full = gf.gen_obs_mask(kd2d_full, self.bdy_msk, self.obs_pts)
        mask_filtered = gf.gen_obs_mask(kd2d_filtered, self.bdy_msk, self.obs_pts)
        self.assertTrue(np.array_equal(mask_full, mask_filtered))
        mask_filtered[0] = (mask_filtered[0]+1)%2
        self.assertFalse(np.array_equal(mask_full, mask_filtered))
    
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    unittest.main()

