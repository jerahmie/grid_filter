"""Unittests for graph_data module"""
import numpy as np
import unittest
from grid_perimeter import graph_data

class TestGraphData(unittest.TestCase):
    """Test case for graph_data"""
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def testTestGraphDataConfig(self):
        """Test the unittest configuration.  This should always pass."""
        self.assertTrue(True)

    def test_mpas_graph(self):
        """Test that MPasGraph type can be instantiated and has correct type"""
        mg = graph_data.MpasGraphData(np.zeros(100), np.zeros(100))
        self.assertIsInstance(mg, graph_data.MpasGraphData)
        self.assertIsInstance(mg.edges, np.ndarray)
        self.assertTrue(np.equal(mg.edges, np.zeros(100)).all())

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
