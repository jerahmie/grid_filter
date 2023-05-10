"""KD Tree Data structure for MPAS grid Data
"""
from typing import List, Tuple

def sort_points(pts: List[Tuple[float, float, int]], dim: int) -> List[Tuple[float, float, int]]:
    """Return a list of sorted points by dimension.

    Keyword arguments:
    pts -- list of (lat, lon, cell_index) points 
    dim -- dimension to sort over. (0 : lat, 1 : lon)
    """
    if dim == 0:
        pts = sorted(pts, key=lambda pt: pt[0])
    elif dim == 1:
        pts = sorted(pts, key=lambda pt: pt[1])
    else:
        raise RuntimeError("Could not sort on index: {dim}".format(dim=dim))
    return pts

def median_point_id(pts: List[Tuple[float, float, int]]) -> Tuple[Tuple[float, float, int], int] :
    """Return the index, point of the median point in list of sorted points.

    Keyword arguments:
    pts -- list of (lat, lon, cell_index) points
    dim -- dimension to search for media (0 : x, 1 : y)
    """
    idx = int((len(pts) - 1) // 2) 

    return pts[idx], idx

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

def build_tree(pts, depth=0) -> Tuple[Node2D, int]:
    """helper function to build the kd tee"""
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

def euclidean_2d_distance_sq(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Calculate the Euclidean squared distance between 2D points, p1 and p2"""
    return (p2[0]-p1[0])**2 + (p2[1]-p1[1])**2

def euclidean_1d_distance_sq(p1: Tuple[float, float], p2: Tuple[float, float], dim) -> float:
    """Calculate the x- or y- projected squared distance between two points"""
    if (dim == 0) or (dim == 1):
        dist_sq = (p2[dim] - p1[dim])**2
    else:
        raise RuntimeError(f'Invalid dimension: {dim}')
    return dist_sq

class KDTree2D():
    """ 2-Dimensional KD Tree.
    """
    def __init__(self, pts: List[Tuple[float, float]]):
        self._points = pts
        self._max_depth = 0
        self._root = build_tree(pts)
        self._find_max_depth()
        self._compares = 0

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
    
    def _nearest_cell(self, qpt: Tuple[float, float], node: Node2D, w:float, depth:int) -> Tuple[float, int]:
        """Descent tree find point closes to given 2D point.
        Keyword arguments:
        qpt -- query point
        w -- min search dimension (i.e. radius), initially larger than domain
        """
        # update compare counter
        self._compares += 1
        # update state variable
        dim = depth%1
        depth += 1
        #print(f'node.data {node.data}')
        # current node
        w_test = euclidean_2d_distance_sq(qpt, node.data)

        print(f'node: {node.data[2]}, w: {w}, w_test: {w_test}')
        nearest_cell = node.data[2]

        # Advance down the tree until closes point is found.
        if (node.left is None) and (node.right is None):
            # leaf node
            if w_test < w:
                nearest_cell = node.data[2] # update nearest_cell
                w = w_test # update min distance
                #print(f'<--> leaf_node, nearest_cell: {nearest_cell}, w: {w}')
        elif (node.left is not None) and (node.right is None):
            # Node has only left child
            #print(f'<--> Node has only left child')
            node = node.left
            w_test_child, nearest_cell_child = self._nearest_cell(qpt, node, w_test, depth)
            if w_test_child < w_test:
                w = w_test_child
                nearest_cell = nearest_cell_child
            #else:
            #    w = w_test
                #nearest_cell = nearest_cell
        elif (node.left is None) and (node.right is not None):
            #print(f'<--> Node had only right child')
            # Node has only right child
            node = node.right
            w_test_child, nearest_cell_child = self._nearest_cell(qpt, node, w_test, depth)
            if w_test_child < w_test:
                w = w_test_child
                nearest_cell = nearest_cell_child
            #else:
            #    w = w_test
                #nearest_cell = nearest_cell
            
        else: # node.left is not None and node.right is not None
            """ Node has left and right child.  This requires a check for query point close to
            dividing plane that could have close points.
            """
            #print(f'<--> Node has left and right')
            if qpt[dim] < node.data[dim]: # left branch
                #print(f' <--> Left Branch')
                w_test_child, nearest_cell_child = self._nearest_cell(qpt, node.left, w_test, depth)
                # handle case where point is close to dividing plane 
                if w_test > euclidean_1d_distance_sq(qpt, node.data, dim):
                    #print(f'  <--> Check alt branch (right)')
                    w_test_child_alt, nearest_cell_child_alt = self._nearest_cell(qpt, node.right, w_test, depth)
                    if w_test_child_alt < w_test_child:
                        w_test_child = w_test_child_alt
                        nearest_cell_child = nearest_cell_child_alt
            else: # right branch
                #print(f' <--> Right Branch')
                w_test_child, nearest_cell_child = self._nearest_cell(qpt, node.right, w_test, depth)
                # handle case where point is close to dividing plane
                if w_test > euclidean_1d_distance_sq(qpt, node.data, dim):
                    #print(f'  <--> Check alt branch (left)')
                    w_test_child_alt, nearest_cell_child_alt = self._nearest_cell(qpt, node.left, w, depth)
                    if w_test_child_alt < w_test_child:
                        w_test_child = w_test_child_alt
                        nearest_cell_child = nearest_cell_child_alt
            if w_test_child < w_test:
                #print('updating w, nearest_cell')
                w = w_test_child
                nearest_cell = nearest_cell_child
            #else:
            #    w = w_test
                #nearest_cell = nearest_cell

        return w, nearest_cell

    @property
    def root(self):
        """Return the root node of the KDTree2D"""
        return self._root

    @property
    def compares(self) -> int:
        """Return the number of compares from last nearest_cell call"""
        return self._compares

    def nearest_cell(self, qpoint: Tuple[float, float]) -> int:
        """Returns the cell nearest to the (lat, lon) point in tree."""
        self._compares = 0
        w, cell = self._nearest_cell(qpoint, self._root, 1.0e10, 0)
        return cell


