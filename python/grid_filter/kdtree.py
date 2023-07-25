"""KD Tree Data structure for MPAS grid Data
"""
from typing import List, Tuple
from .kdtree_util import sort_points, median_point_id, euclidean_2d_distance_sq, euclidean_1d_distance_sq

class Node2D():
    """KD-Tree Node"""
    def __init__(self, data, left = None, right=None):
        self._left = left
        self._right = right
        self._data = data  # cell position (lat, lon, cell_index)

    def __str__(self):
        """Pretty-print the node data"""
        return f'({self._data})'
    
    def __repr__(self):
        """Define the repr string."""
        return f'(Node2D, \'{self._data}\', left={self._left}, right={self._right})'
    
    @property
    def data(self):
        """Return the data of the current node"""
        return self._data

    @property
    def left(self):
        """Return the left node"""
        return self._left

    @property
    def right(self):
        """Return the right node"""
        return self._right

def build_tree(pts, depth=0) -> Node2D:
    """Helper function to build a 2D kd tree.
    
    Recursive algorithm to create 2D KDTree from List of points.
    List sorting dimension alternates according to current depth of tree.

    Keyword Arguments:
    pts   -- List of 2D points 
    depth -- current depth of tree
    """
    if len(pts) == 1:
        return Node2D(pts[0])
    else:
        dim = depth%2
        depth += 1
        sorted_pts = sort_points(pts, dim)
        (med, idx) = median_point_id(sorted_pts)
        if idx > 0:
            left_subtree = build_tree(sorted_pts[:idx], depth)
        else: 
            left_subtree = None
        if (idx+1) < len(pts):
            right_subtree = build_tree(sorted_pts[idx+1:], depth)
        else:
            right_subtree = None

        return Node2D(med, left=left_subtree, right=right_subtree)

def find_max_depth(node:Node2D, depth:int=0)-> int:
    """find the maximum depth of tree
    """
    depth += 1
    left_depth = depth
    right_depth = depth
    if node.left is not None:
        left_depth = find_max_depth(node.left, depth)
    if node.right is not None:
        right_depth = find_max_depth(node.right, depth)

    return max(left_depth, right_depth)

class KDTree2D():
    """ 2-Dimensional KD Tree.
    """
    def __init__(self, pts: List[Tuple[float, float]]):
        self._points = pts
        self._max_depth = 0
        self._root = build_tree(pts)
        self._find_max_depth()
        self._compares = 0
        self._visited_points = []

    def __str__(self):
        """Display string for KDTree2D class"""
        return f'KDTree2D({self._max_depth})'

    def __repr__(self):
        """"""
        return f'<KDTree2D size {len(self._points)} with depth {self._max_depth}>'


    def _find_max_depth(self):
        """Traverse tree (dfs) to find max_depth"""
        self._max_depth = find_max_depth(self._root)

    @property
    def max_depth(self):
        """Return the depth of the KD tree"""
        return self._max_depth
    
    def _nearest_cell(self, qpt: Tuple[float, float], node: Node2D, depth:int) -> Tuple[float, int]:
        """Descent tree find point closes to given 2D point.
        Keyword arguments:
        qpt -- query point
        node -- current node in KD-tree
        depth -- current depth in tree
        """
        # update compare counter
        self._compares += 1
        # update state variable
        dim = depth%2
        depth += 1
        self._visited_points.append(node._data[2])

        w_node = euclidean_2d_distance_sq(qpt, node.data)

        if node.left is None and node.right is None:
            """ leaf node """
            return w_node, node.data[2]

        elif node.left is not None and node.right is None:
            """Node with only right child node"""
            w_left, nearest_cell_left = self._nearest_cell(qpt, node.left, depth)
            if w_left < w_node:
                w = w_left
                nearest_cell = nearest_cell_left
            else:
                w = w_node
                nearest_cell = node.data[2]
            return w, nearest_cell

        elif node.left is None and node.right is not None:
            """Node with only left child node"""
            w_right, nearest_cell_right = self._nearest_cell(qpt, node.right, depth)
            if w_right < w_node:
                w = w_right
                nearest_cell = nearest_cell_right
            else:
                w = w_node
                nearest_cell = node.data[2]
            return w, nearest_cell

        else:
            if qpt[dim] < node.data[dim]:
                w_left, nearest_cell_test = self._nearest_cell(qpt, node.left, depth)
                if w_left < w_node:
                    w = w_left
                    nearest_cell = nearest_cell_test
                else:
                    w = w_node
                    nearest_cell = node.data[2]
                if euclidean_1d_distance_sq(qpt, node.data, dim) < w and node.right is not None:
                    w_test_alt, nearest_cell_test_alt = self._nearest_cell(qpt, node.right, depth)
                    if w_test_alt < w:
                        w = w_test_alt
                        nearest_cell = nearest_cell_test_alt
                
            elif qpt[dim] > node.data[dim]: # qpt[dim] >= node.data[dim]
                w_right, nearest_cell_test = self._nearest_cell(qpt, node.right, depth)
                if w_right < w_node:
                    w = w_right
                    nearest_cell = nearest_cell_test
                else:
                    w = w_node
                    nearest_cell = node.data[2]
                if euclidean_1d_distance_sq(qpt, node.data, dim) < w and node.left is not None:
                    w_test_alt, nearest_cell_test_alt = self._nearest_cell(qpt, node.left, depth)
                    if w_test_alt < w:
                        w = w_test_alt
                        nearest_cell = nearest_cell_test_alt

            else:
                print("!!!!! TODO: both search paths. qpt[dim] is at bisecion point !!!!")

            return w, nearest_cell

    @property
    def root(self):
        """Return the root node of the KDTree2D"""
        return self._root

    @property
    def compares(self) -> int:
        """Return the number of compares from last nearest_cell call"""
        return self._compares

    @property
    def visited_points(self) -> List[int]:
        """Return list of points in visited path"""
        return self._visited_points

    def nearest_cell(self, qpoint: Tuple[float, float]) -> int:
        """Returns the cell nearest to the (lat, lon) point in tree."""
        self._compares = 0
        self._visited_points = []
        w = euclidean_2d_distance_sq(qpoint, self._root.data)
        w, cell = self._nearest_cell(qpoint, self._root, 0)
        return cell


