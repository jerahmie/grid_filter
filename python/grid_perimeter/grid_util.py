"""
grid perimeter caluculation 
"""
import os
import numpy as np
from netCDF4 import Dataset

class MpasGrid(object):
    """ MPAS Grid class
    """
    def __init__(self, filename: str=""):
        self._filename = filename
        self._dataset = None
        self._ncells = 0
        self._nvertices = 0
        self._nedges = 0
        if os.path.exists(filename):
            self._load_dataset()
    
    def _load_dataset(self):
        """Loads grid data from netCDF4 file
        """
        if os.path.exists(self._filename):
            self._dataset = Dataset(self._filename, 'r')
            self._read_ncells()
            self._read_nvertices()
            self._read_nedges()
        else:
            print("Warning: Could not file")
            
    def _read_ncells(self):
        """Read the number of Cells in grid"""
        self._ncells = self._dataset.dimensions['nCells'].size

    @property
    def ncells(self):
        return self._ncells

    def _read_nvertices(self):
        """Read the number of Vertices in the grid"""
        self._nvertices = self._dataset.dimensions['nVertices'].size

    @property
    def nvertices(self):
        return self._nvertices

    def _read_nedges(self):
        """Read the number of edges in the grid"""
        self._nedges = self._dataset.dimensions['nEdges'].size

    @property
    def nedges(self):
        return self._nedges

    def mpas_interior_cell(self, cell_id: int) -> bool:
        """Return true if cell_id is index of cell in grid interior. False if edge.    
        Keyword arguments:
        ncds    -- netCDF4 dataset
        cell_id -- id of cell in grid
        """
        if cell_id < 0 or cell_id >= self._ncells:
            print("Warning: cell_id out of range of nCells (", ncells, ")")
        else:
            cells_on_cell = self._dataset.variables["cellsOnCell"][cell_id]
            print("Cells on cell: ", cells_on_cell)
            return cells_on_cell


