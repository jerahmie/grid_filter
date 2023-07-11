"""Unittesting to read and process observation points.
"""
import os
import numpy as np
import unittest
import grid_filter as gf

class TestObsPoints(unittest.TestCase):
    """Test class for test point observations."""
    @classmethod
    def setUpClass(cls):
        this_dir = os.path.abspath(os.path.dirname(__file__))
        cls.obsfile = os.path.join(this_dir, 'satwind_obs_2019050100.h5')
        cls.n_points = 287290

    def setUp(self):
        pass

    def test_setup_tests(self):
        """Ensure the test class is configured correctly.
        This should always pass.
        """
        self.assertTrue(True)

    def test_read_obs(self):
        self.assertTrue(os.path.exists(self.obsfile))
        lonc = gf.read_h5data(self.obsfile, 'MetaData', 'longitude')
        self.assertEqual(np.size(lonc), self.n_points)
        latc = gf.read_h5data(self.obsfile, 'MetaData', 'latitude')
        self.assertEqual(np.size(latc), self.n_points)
        lat_lon = gf.obs_points(self.obsfile)
        self.assertEqual(np.shape(lat_lon), (2,self.n_points))
        
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
