"""Unittests for kdtree module"""
import os
import unittest
from random import uniform
from grid_perimeter import * 

def dist2(p1, p2):
    """return 2D Euclidean squared distance between two points"""
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2


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

    def test_KDTree2D_root(self):
        """KDTree2D.root should return the root node."""
        kd2 = KDTree2D(self.ptsi)
        # Root should be a Node2D object
        self.assertTrue(isinstance(kd2.root, Node2D))
        # Root should be data index 302
        self.assertEqual(kd2.root.data[2], 302)

    def test_KDTree2D_str(self):
        """Test string representation of KDTree2D"""
        kd2 = KDTree2D(self.p)
        self.assertEqual("KDTree2D(3)", kd2.__str__())

    def test_KDTree2D_repr(self):
        """Test the repr string of KDTree2D"""
        kd2 = KDTree2D(self.p)
        self.assertEqual("<KDTree2D size 4 with depth 3>", kd2.__repr__())


    def test_KDTree2D_search_small(self):
        """Test searching a small KDTree"""
        #[(1.1,-2.2, 0), (3.3, 4.4, 1), (-1.1, 2.2, 2), (-6.6, 7.7, 3)]
        # Single element tree. All points return element 0
        kd2_1 = KDTree2D([(1.1, -2.2, 0)])
        self.assertEqual(kd2_1.nearest_cell((0.0, 0.0)), 0)
        self.assertEqual(kd2_1.nearest_cell((-1.1, -1.1)), 0)
        self.assertEqual(kd2_1.nearest_cell((1.1, -2.2)), 0)
        self.assertEqual(kd2_1.nearest_cell((2.2, 2.2)), 0)

        # Tree with root and right element
        kd2_2_right = KDTree2D([(1.1, -2.2, 0), (3.3, 0.0, 1)])
#        distances = [(28.317347386040694, 12.862417893109328),
#                 (53.834161276403194, 19.675703562818097),
#                 (45.74066535602422, 33.28861241313738),
#                 (48.324752047135874, 15.601688034661843),
#                 (23.092996370871923, 2.870908506384719),
#                 (11.107371465165858, 29.639321545091487),
#                 (11.340396317358065, 37.84658181311603),
#                 (14.679427788161213, 7.388062166704951),
#                 (6.523763142562467, 17.133126688664607),
#                 (2.5112447490924823, 7.794942801546315)]
        qpts = [(1.5066388771313957, 3.1058450985348234),
                (4.632396760745577, 4.230889083251036),
                (-0.4525580479544846, 4.382570080428767),
                (4.946858941332163, 3.590201061502844),
                (4.479655026468684, 1.2162740336420432),
                (-2.0370636763168193, -1.0747431600299153),
                (-2.231291579093906, -2.6928414881238147),
                (4.931286990286118, -2.1741584399551495),
                (-0.8085870883241171, -0.502631899426369),
                (0.5965631013100179, -0.6974035677767985)]
        nearest_pt = [1, 1, 1, 1, 1, 0, 0, 1, 0, 0]
        for i,qtest in enumerate(qpts):
            self.assertEqual(kd2_2_right.nearest_cell(qtest), nearest_pt[i])

        # Tree with root and left element
        kd2_2_left = KDTree2D([(0.5, 2.2, 0), (-1.1, -2.2, 1), (2.3, 3.4, 2)])
        # force root and left element
        kd2_2_left.root._right = None
        nearest_pt = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
        for i,qtest in enumerate(qpts):
            self.assertEqual(kd2_2_left.nearest_cell(qtest), nearest_pt[i])
        # distacncees kd2_2lr
        #[(1.8338771714919206, 34.94655844541884, 0.7159489773353201), (21.20121345668877, 74.21670702368372, 6.130451318202207), (5.6709789907056924, 43.74940994502449, 8.542019770312796), (21.70721343550944, 70.09093138899738, 7.042038699106828), (16.80537090658436, 42.803478487334125, 9.519555130556194), (17.16063486184893, 2.1442912893718535, 38.83344768066127), (31.399851517934948, 1.5227133693448789, 57.655320774170164), (38.76956644810987, 36.377090545420124, 37.994913538972206), (9.016619351525573, 2.9659799539363525, 24.89384942811568), (8.40427186710033, 5.136122394856561, 19.690413265048576)]
        nearest_pt = [2, 2, 0, 2, 2, 1, 1, 1, 1, 1]
        kd2_2lr = KDTree2D([(0.5, 2.2, 0), (-1.1, -2.2, 1), (2.3, 3.4, 2)])
        for i,qtest in enumerate(qpts):
            self.assertEqual(kd2_2lr.nearest_cell(qtest), nearest_pt[i])

    def test_KDTree2D_small_random(self):
        """Create a small KDTree2D and find nearest points on randomized data sets"""
        tree_pts = [(uniform(-2.0,2.0), uniform(-2.0,2.0), i) for i in range(3)]
        kd2_rand = KDTree2D(tree_pts)
        qpts = [(uniform(-2.0, 2.0), uniform(-2.0, 2.0)) for i in range(100)]
        d0 = [dist2(tree_pts[0], q) for q in qpts]
        d1 = [dist2(tree_pts[1], q) for q in qpts]
        d2 = [dist2(tree_pts[2], q) for q in qpts]
        dmi = [d.index(min(d)) for d in list(zip(d0, d1, d2))]
        for i,qpt in enumerate(qpts):
            self.assertEqual(kd2_rand.nearest_cell(qpt), dmi[i])

    @unittest.skip
    def test_KDTree2D_search(self):
        """Search the KDTree2D for nearest cell."""
        kd2 = KDTree2D(self.ptsi)
        test_pt1 = (0.86, 4.76)
        nearest_cell_id = kd2.nearest_cell(test_pt1)
        self.assertEqual(nearest_cell_id, 225)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
