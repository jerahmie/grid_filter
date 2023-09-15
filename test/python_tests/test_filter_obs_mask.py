'''Unittesting to filter data and save output.
'''
import os
import numpy as np
import unittest
import h5py
import grid_filter as gf

# Expected Dimensions
NOBS_SATWIND = 287290
NFILTERED_POINTS_SATWIND = 274
H5_DATASET_TYPE = h5py._hl.dataset.Dataset
H5_GROUP_TYPE = h5py._hl.group.Group

#def find_dataset_address(fh: h5py._hl.files.File, addr:str="/" )->str:
#    '''Recursively find the address of each Dataset
#    '''
#    try:
#
#    except:
#        print("HDF5 file handle Error.")
#
#    return addr 

class TestObsFilter(unittest.TestCase):
    '''Test class for test point observations.
    '''
    @classmethod
    def setUpClass(cls):
        this_dir = os.path.abspath(os.path.dirname(__file__))
        cls.obsfile = os.path.join(this_dir, 'satwind_obs_2019050100.h5')
        cls.n_points = NOBS_SATWIND
        with h5py.File(cls.obsfile) as fh:
            cls.latc = fh['/MetaData/latitude'][:]
            cls.lonc = fh['/MetaData/longitude'][:]
        cls.obs_pts = gf.obs_points(cls.obsfile)
        cls.static_file = os.path.join(this_dir, 'Manitowoc.static.nc')
        mpg = gf.MPASGrid(cls.static_file)
        pts = mpg.cell_points()
        cls.bdy_msk = mpg.bdy_mask_cells
        ptsi = [(pts[i][0], pts[i][1], i) for i in range(len(pts))]
        ptsi_filtered, _ = gf.filter_bdy_mask_cell(ptsi, cls.bdy_msk, {6,7})
        cls.kd2d = gf.KDTree2D(ptsi)

    def setUp(self):
        # netcdf regional grid file
        this_dir = os.path.abspath(os.path.dirname(__file__))

    def test_setup_tests(self):
        '''Ensure the test class is configured correctly.
        This should always pass.
        '''  
        self.assertTrue(True)

    def test_obs_filter_1d_small(self):
        '''Test filter 1d on a small dataset.
        '''
        a = np.arange(101)
        b = np.ones(len(a))
        c = np.zeros(len(a))
        vfunc = np.vectorize(lambda x, mask: x if mask else 0)
        self.assertEqual(np.sum(vfunc(a,b)), 5050)
        self.assertEqual(np.sum(vfunc(a,c)), 0) 
        filtered_output = vfunc(a,c)
        filtered_output = filtered_output[filtered_output != 0]
        self.assertEqual(np.shape(filtered_output), (0,))
        balt = np.vectorize(lambda a: 1 if a%2 == 0 else 0)
        filtered_output2 = vfunc(a, balt(a))
        filtered_output2 = filtered_output2[filtered_output2 != 0]
        self.assertEqual(np.shape(filtered_output2), (50,))
        self.assertEqual(np.shape(gf.filter_obs_by_mask(a, balt(a))), (51,))

    @unittest.skip
    def test_obs_filter_kd2d(self):
        '''Test filtering observations with calculated mask.
        '''
        min_max = gf.find_tree_min_max(self.kd2d.root) 
        mask_out = gf.filter_main(self.static_file, self.obsfile)
        self.assertEqual(np.sum(mask_out), NFILTERED_POINTS_SATWIND)
        fh = h5py.File(self.obsfile)
        obs_attributes_keys = fh.attrs.keys()
        keys = fh.keys()
        for key in keys:
            if type(fh[key]) == H5_GROUP_TYPE:
                print(f'Found Group {key}')
                print(fh[key].keys())
            elif type(fh[key]) == H5_DATASET_TYPE:
                print(f'Found Dataset {key}')
            else:
                print('Unknown type found for key: {key}.')

        fh.close() 

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
