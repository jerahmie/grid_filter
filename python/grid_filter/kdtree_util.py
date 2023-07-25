""" Utility and helper functions for KD-Tree building
"""
from typing import Tuple, List

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

def median_point_id(pts: List[Tuple[float, float, int]]) -> Tuple[Tuple[float, float, int], int]:
    """Return the index, point of the median point in list of sorted points.

    Keyword arguments:
    pts -- list of (lat, lon, cell_index) points
    dim -- dimension to search for media (0 : x, 1 : y)
    """
    idx = int((len(pts) - 1) // 2)

    return pts[idx], idx

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
