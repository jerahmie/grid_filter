'''Unittests for kdtree module validation.
'''
import os
import unittest
import grid_filter as gf
import h5py
import netCDF4
import numpy as np

PRECISION = 0.0001

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
        ptsi = [(180.0/np.pi*cls.pts[i][0], 180.0/np.pi*cls.pts[i][1], i) for i in range(len(cls.pts))]
        cls.kd2d= gf.KDTree2D(cls.pts)

    def setUp(self):
        pass

    def test_TestKDTreeValidation(self):
        '''Test that the TestDKTreeValidation class is setup correctly.'''
        self.assertTrue(True)
        self.assertTrue(os.path.exists(self.obs_file))
        self.assertTrue(os.path.exists(self.static_file))

    @unittest.skip("Long test")
    def test_bdy_msk_types(self):
        '''Test full kdtree'''
        ptsi = [(180.0/np.pi*self.pts[i][0], 180.0/np.pi*self.pts[i][1], i) for i in range(len(self.pts))]
        self.assertEqual(len(ptsi), 441)
        kd2d_full = gf.KDTree2D(ptsi)

        ptsi_filtered, _ = gf.filter_bdy_mask_cell(ptsi, self.bdy_msk, {6,7})
        print(f'len(self.bdy_msk) {len(self.bdy_msk)}')
        self.assertEqual(len(ptsi_filtered), 136)
        kd2d_filtered = gf.KDTree2D(ptsi_filtered)
        mask_full = gf.gen_obs_mask(self.kd2d_full, self.bdy_msk, self.obs_pts)
        mask_filtered = gf.gen_obs_mask(kd2d_filtered, self.bdy_msk, self.obs_pts)
        self.assertTrue(np.array_equal(mask_full, mask_filtered))
        mask_filtered[0] = (mask_filtered[0]+1)%2
        self.assertFalse(np.array_equal(mask_full, mask_filtered))
   
    def test_find_min_max(self):
        '''Test find min and max x,y points in kdtree.
        '''
        max_lat = max([pt[0] for pt in self.pts[:]])
        min_lat = min([pt[0] for pt in self.pts[:]])
        max_lon = max([pt[1] for pt in self.pts[:]])
        min_lon = min([pt[1] for pt in self.pts[:]])
        print(f'min_lat: {min_lat :.2f}, max_lat: {max_lat :.2f}, min_lon: {min_lon :.2f}, max_lon: {max_lon :.2f}')
        node_stack = []
        node_stack.append(self.kd2d.root)
        kd_minlat = node_stack[0].left.data[0]
        kd_minlon = node_stack[0].right.data[1]
        kd_maxlat = kd_minlat
        kd_maxlon = kd_minlon
        while len(node_stack) > 0:
            curr_node = node_stack.pop(-1)
            if curr_node.data[0] < kd_minlat:
                kd_minlat = curr_node.data[0]
            if curr_node.data[0] > kd_maxlat:
                kd_maxlat = curr_node.data[0]
            if curr_node.data[1] < kd_minlon:
                kd_minlon = curr_node.data[1]
            if curr_node.data[1] > kd_maxlon:
                kd_maxlon = curr_node.data[1]
            if curr_node.left is not None:
                node_stack.append(curr_node.left)
            if curr_node.right is not None:
                node_stack.append(curr_node.right)

        print(f'kd_minlat {kd_minlat :.2f}, kd_maxlat {kd_maxlat :.2f} , kd_minlon {kd_minlon :.2f}, kd_maxlon {kd_maxlon :.2f}')
        self.assertTrue(np.abs(kd_minlat-min_lat) < PRECISION)
        self.assertTrue(np.abs(kd_maxlat-max_lat) < PRECISION)
        self.assertTrue(np.abs(kd_minlon-min_lon) < PRECISION)
        self.assertTrue(np.abs(kd_maxlon-max_lon) < PRECISION)


    def test_find_tree_min_max(self):
        ''' Use find_tree_min_max function to find min/max
        '''
        max_lat = max([pt[0] for pt in self.pts[:]])
        min_lat = min([pt[0] for pt in self.pts[:]])
        max_lon = max([pt[1] for pt in self.pts[:]])
        min_lon = min([pt[1] for pt in self.pts[:]])
        print(gf.find_tree_min_max(self.kd2d.root))
        self.assertTrue(np.abs(gf.find_tree_min_max(self.kd2d.root)[0][0] - min_lat) < PRECISION)
        self.assertTrue(np.abs(gf.find_tree_min_max(self.kd2d.root)[0][1] - max_lat) < PRECISION)
        self.assertTrue(np.abs(gf.find_tree_min_max(self.kd2d.root)[1][0] - min_lon) < PRECISION)
        self.assertTrue(np.abs(gf.find_tree_min_max(self.kd2d.root)[1][1] - max_lon) < PRECISION)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    unittest.main()

