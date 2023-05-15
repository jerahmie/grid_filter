"""Unittests for graph_data module"""
import os
import numpy as np
import unittest
from grid_filter import graph_data

class TestGraphData(unittest.TestCase):
    """Test case for graph_data"""
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        this_dir = os.path.abspath(os.path.dirname(__file__))
        self.ncfile = os.path.join(this_dir, 'Manitowoc.static.nc')
        self.mp = graph_data.MpasGraph(self.ncfile)

    def testTestGraphDataConfig(self):
        """Test the unittest configuration.  This should always pass."""
        self.assertTrue(True)

    def test_mpas_graph_data(self):
        """Test that MPasGraphData class can be instantiated and has correct type."""
        mgd = graph_data.MpasGraphData(np.zeros(100), np.zeros(100))
        self.assertIsInstance(mgd, graph_data.MpasGraphData)
        self.assertIsInstance(mgd.edges, np.ndarray)
        self.assertTrue(np.equal(mgd.edges, np.zeros(100)).all())

    def test_mpas_graph(self):
        """Test MPasGraph class can be instantiated and has correct type."""
        mg = graph_data.MpasGraph(self.ncfile)
        self.assertIsInstance(mg, graph_data.MpasGraph)
        self.assertTrue(hasattr(mg, 'populate_edges'))
        self.assertTrue(hasattr(mg, '_nc_filename'))
        self.assertEqual(mg._nc_filename, self.ncfile)
    
    def test_populate_edges(self):
        """Test MpasGraph populate edges"""
        mpd = graph_data.MpasGraphData()
        self.mp.populate_edges(mpd)
        

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
