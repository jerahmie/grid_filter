"""KD Tree Data structure for MPAS grid Data
"""
from typing import List, Tuple

def sort_points(pts: List[Tuple[float, float]], dim: int) -> List[Tuple[float, float]]:
    """Return a list of sorted points by dimension.

    Keyword arguments:
    pts -- list of (x, y) points 
    dim -- dimension to sort over. (0 : x, 1 : y)
    """
    if dim == 0:
        pts = sorted(pts, key=lambda pt: pt[0])
    elif dim == 1:
        pts = sorted(pts, key=lambda pt: pt[1])
    else:
        raise RuntimeError("Could not sort on index: {dim}".format(dim=dim))
    return pts

def median_point_id(pts: List[Tuple[float, float]]) -> Tuple[Tuple[float, float], int] :
    """Return the index, point of the median point in list of points.

    Keyword arguments:
    pts -- list of (x, y) points
    dim -- dimension to search for media (0 : x, 1 : y)
    """
    idx = int((len(pts) - 1) // 2) 

    return pts[idx], idx

class Node2D():
    """KD-Tree Node"""
    def __init__(self, data, left = None, right=None):
        self.left = left
        self.right = right
        self.data = data

    def __str__(self):
        """Pretty-print the node data"""
        return f'({self.data})'
    
    def __repr__(self):
        """Define the repr string."""
        return f'(Node2D, \'{self.data}\', left={self.left}, right={self.right})'

def build_tree(pts, depth=0) -> Node2D:
    """helper function to build the kd tee"""
    if len(pts) == 1:
        return Node2D(pts[0])
    else:
        (med, idx) = median_point_id(pts)
        depth += 1
        dim = depth%2
        if idx > 0:
            left_subtree = build_tree(sort_points(pts[:idx], dim), depth)
        else: 
            left_subtree = None
        if (idx+1) < len(pts):
            right_subtree = build_tree(sort_points(pts[idx+1:], dim), depth)
        else:
            right_subtree = None
        return Node2D(med, left=left_subtree, right=right_subtree)

class KDTree2D():
    """ 2-Dimensional KD Tree.
    """
    def __init__(self, pts: List[Tuple[float, float]]):
        self._points = pts
        self._root = None
    