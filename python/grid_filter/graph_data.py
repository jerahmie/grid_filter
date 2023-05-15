"""graph_data.py
Data classes and helper functions to represent meshes and edges of MPAS grid.
"""
from dataclasses import dataclass, field
from typing import Optional
import numpy as np
from netCDF4 import Dataset

@dataclass
class MpasGraphData:
    """Graph representation of MPAS cells, vertices, and edges.
    """
    edges: Optional[np.ndarray] = None
    nodes: Optional[np.ndarray] = None


class MpasGraph:
    """ A class to contain functions that operate on  our MpasGraphData 
    """
    def __init__(self, nc_file: str):
        self._nc_filename = nc_file
        self._dataset = Dataset(nc_file, 'r')

    def populate_edges(self, mpas_data: MpasGraphData) -> None:
        """Load edges from Dataset into graph data object"""
        pass