"""graph_data.py
Data classes and helper functions to represent meshes and edges of MPAS grid.
"""
from dataclasses import dataclass
import numpy as np

@dataclass
class MpasGraphData:
    """Graph representation of MPAS cells, vertices, and edges.
    """
    edges: np.ndarray
    nodes: np.ndarray

class MpasGraph:
    """
    """
    def __init__(self):
        pass
