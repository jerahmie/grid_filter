"""Unittests for kdtree module"""
import os
import unittest
from grid_perimeter import * 

class TestKDTree2D(unittest.TestCase):
    """Test case for 2D KD Tree"""
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        # a non-trivial list of points
        self.p = [(1.1,-2.2, 0), (3.3, 4.4, 1), (-1.1, 2.2, 2), (-6.6, 7.7, 3)]
        # netcdf regional grid file
        this_dir = os.path.abspath(os.path.dirname(__file__))
        self.grid_file = os.path.join(this_dir, 'Manitowoc.static.nc')
        mpg = MPASGrid(self.grid_file)
        pts = mpg.cell_points()
        self.ptsi = [(pts[i][0], pts[i][1], i) for i in range(len(pts))]

    def test_kdtree2d(self):
        """Test create kdtree"""
        p = [(1.1, 2.2, 0), (3.3, 4.4, 1)]
        a = KDTree2D(p)
        self.assertTrue(isinstance(a, KDTree2D))

    def test_sort_points(self):
        """Test ability to sort points over x- or y- points."""
        spx = [(-6.6, 7.7, 3), (-1.1, 2.2, 2), (1.1, -2.2, 0), (3.3, 4.4, 1)]
        spy = [(1.1,-2.2, 0), (-1.1,2.2, 2), (3.3, 4.4, 1), (-6.6, 7.7, 3)]

        # single point should already be sorted
        self.assertEqual([(1.1, 2.2)], sort_points([(1.1, 2.2)], 0))
        self.assertEqual([(1.1, 2.2)], sort_points([(1.1, 2.2)], 1))

        # empty list should return empty list
        self.assertEqual([], sort_points([],0)) 
        # sort multi-point list
        self.assertEqual(spx, sort_points(self.p,0))
        self.assertEqual(spy, sort_points(self.p,1))

        # sorting over wrong index should raise exception
        with self.assertRaises(RuntimeError):
            sort_points(self.p,2)

    def test_median_point_id(self):
        """Test find media point from sorted list."""
        self.assertEqual(((-1.1, 2.2, 2), 1), median_point_id(sort_points(self.p, 0)))
        p5 = self.p
        p5.append((-10.0, -10.0))
        self.assertEqual(((-1.1, 2.2, 2), 2), median_point_id(sort_points(p5, 0)))
        # single point list
        self.assertEqual(((-1.1, 2.2, 2), 0), median_point_id([(-1.1, 2.2, 2)]))
        self.assertEqual(((0, 0, 0), 0), median_point_id([(0, 0, 0)]))
    
    def test_median_point_medium(self):
        """Test median point on medium sized data set."""
        mpg = MPASGrid(self.grid_file)
        pts = mpg.cell_points()
        self.assertEqual(len(pts), 441)

    def test_kdtree2d_node(self):
        """Test the constuction of kdtree node"""
        nroot = Node2D((1.0, 2.0, 0))
        self.assertTrue(isinstance(nroot, Node2D))
        self.assertEqual('((1.0, 2.0, 0))', str(nroot))
        self.assertEqual('(Node2D, \'(1.0, 2.0, 0)\', left=None, right=None)', repr(nroot))

    def test_build_tree(self):
        """Test the construction of a kd tree."""
        pts = [(0.0, 1.1, 0), (1.1, -1.0, 1), (2.2, -1.1, 2), (3.3, 4.4, 3)]
        a = build_tree(pts)
        self.assertEqual("(Node2D, '(1.1, -1.0, 1)', left=((0.0, 1.1, 0)), right=((2.2, -1.1, 2)))", repr(a))

    def test_build_big_tree(self):
        """Test building a meaningful tree from data."""
        mpg = MPASGrid(self.grid_file)
        pts = mpg.cell_points()
        self.assertEqual(len(pts), 441)
        ptsi = [(pts[i][0], pts[i][1], i) for i in range(len(pts))]
        kdtree = build_tree(ptsi)

        print('kdtree: ', repr(kdtree))
        print('kdtree.left: ', repr(kdtree.left))
        print('kdtree.right: ', repr(kdtree.right))
        self.assertEqual(repr(kdtree), '(Node2D, \'(0.7671914100646973, 4.665992736816406, 302)\', left=((0.7320756316184998, 4.751560211181641, 154)), right=((0.8601444363594055, 4.75323486328125, 225)))')

    def test_KDTree2D(self):
        """Test the KDTree2D Class and methods"""
        pts1 = [(0.0, 1.1, 0)]
        kd2d1pt = KDTree2D(pts1)
        self.assertTrue(isinstance(kd2d1pt, KDTree2D))
        self.assertEqual(kd2d1pt.max_depth, 1)
        pts3 = [(0.0, 1.1, 0), (1.1, -1.0, 1), (2.2, -1.1, 2)]
        kd2d3pt = KDTree2D(pts3)
        self.assertEqual(kd2d3pt.max_depth, 2)

    def test_KDTree2D_medium(self):
        """Test the KDTree2D Class and methods"""
        kd2 = KDTree2D(self.ptsi)
        self.assertEqual(kd2.max_depth, 9)

    def test_KDTree2D_search(self):
        """Search the KDTree2D for nearest cell."""
        kd2 = KDTree2D(self.ptsi)
        test_pt1 = (0.86, 4.76)
        nearest_cell_id = kd2.nearest_cell(test_pt1)
        print(self.ptsi[nearest_cell_id], test_pt1)
        self.assertEqual(nearest_cell_id, 225)

    def test_KDTree2D_root(self):
        """KDTree2D.root should return the root node."""
        kd2 = KDTree2D(self.ptsi)
        # Root should be a Node2D object
        self.assertTrue(isinstance(kd2.root, Node2D))
        # Root should be data index 302
        self.assertEqual(kd2.root.data[2], 302)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
