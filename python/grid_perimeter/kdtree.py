"""KD Tree Data structure for MPAS grid Data
"""
from typing import List, Tuple

def sort_points(pts: List[Tuple[float, float]], idx: int) -> List[Tuple[float, float]]:
    """Return a list of sorted points by index
    """
    pass

class KDTree2D():
    """ 2-Dimensional KD Tree.
    """
    def __init__(self, pts: List[Tuple[float, float]]):
        self._points = pts

