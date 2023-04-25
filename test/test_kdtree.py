"""Unittests for kdtree module"""
import unittest
from grid_perimeter import KDTree2D

class TestKDTree2D(unittest.TestCase):
    """Test case for 2D KD Tree"""
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_kdtree2d(self):
        """Test create kdtree"""
        p = [(1.1, 2.2), (3.3, 4.4)]
        a = KDTree2D(p)
        self.assertTrue(isinstance(a, KDTree2D))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()

