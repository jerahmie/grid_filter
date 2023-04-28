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
        # state variables
        self._curr_depth = 0 # current depth in tree
        self._curr_dim = 0   # kd dimension 
        self._curr_node = self._root # current tree node

    def _find_max_depth(self):
        """Traverse tree (dfs) to find max_depth"""
        self._max_depth = find_max_depth(self._root)

    @property
    def max_depth(self):
        """Return the depth of the KD tree"""
        return self._max_depth
    
    def _nearest_cell(self, point: Tuple[float, float]) -> int:
        """Descent tree find point closes to given 2D point."""
        # update state variable
        self._curr_depth += 1
        self._curr_dim = self._curr_depth%2

        # calculate distances relevant to find nearest point
        dsq = euclidean_1d_distance_sq(point,self._curr_node.data, self._curr_dim)
        if self._curr_node.left is not None:
            dsq_left = euclidean_1d_distance_sq(point, self._curr_node.left.data, self._curr_dim)
        if self._curr_node.right is not None:
            dsq_right = euclidean_1d_distance_sq(point, self._curr_node.right.data, self._curr_dim)

        # Advance down the tree until closes point is found.
        if (self._curr_node.left is None) and (self._curr_node.right is None):
            nearest_cell = self._curr_node.data[2]
        elif (self._curr_node.left is not None) and (self._curr_node.right is None):
            if dsq_right < dsq:
                self._curr_node = self._curr_node.right
                nearest_cell = self._nearest_cell(point) 
            else:
                nearest_cell = self._curr_node.data[2]
        elif (self._curr_node.left is None) and (self._curr_node.right is not None):
            if dsq_left < dsq:
                self._curr_node = self._curr_node.left
                nearest_cell = self._nearest_cell(point)
        else:
            if (dsq_left < dsq) and (dsq_right < dsq):
                if (dsq_left < dsq_right):
                    self._curr_node = self._curr_node.left
                    nearest_cell = self._nearest_cell(point)
                else:
                    self._curr_node = self._curr_node.right
                    nearest_cell = self._nearest_cell(point)
            elif (dsq_left > dsq) and (dsq_right > dsq):
                nearest_cell = self._curr_node.data[2]
            elif (dsq_left < dsq) and (dsq_right > dsq):
                self._curr_node = self._curr_node.left
                nearest_cell = self._nearest_cel(point)
            else: # (dsq_left < dsq) and (dsq_right > dsq):
                self._curr_node = self._curr_node.right
                nearest_cell = self._nearest_cel(point)
        return nearest_cell


    def nearest_cell(self, point: Tuple[float, float]) -> int:
        """Returns the cell nearest to the (lat, lon) point in tree."""
        self._curr_depth = 0 # reset depth state variable
        self._curr_dim = 0 # reset kd dimension state variable
        self._curr_node = self._root
        return self._nearest_cell(point)
    


