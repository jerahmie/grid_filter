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
    """ A class to contain functions that operate on  our MpasGraphData 
    """
    def __init__(self, nc_file: str):
        self._nc_filename = nc_file
     

    def populate_edges(mpas_data: MpasGraphData) -> None:
        pass