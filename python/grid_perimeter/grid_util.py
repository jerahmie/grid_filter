"""
grid perimeter caluculation 
"""
import os
from typing import List
from netCDF4 import Dataset

gt_zero = lambda x: x>0      # filter function for integers greater than zero
lt_one = lambda ix: ix[1]<1.0     # filter function for values under 1.0
mpas_indices = lambda ix: ix[0]   # index from enumerated tuple element

def len_non_zero(values: list) -> int:
    """Helper to find the number of non-zeros in a list"""
    return len(list(filter(gt_zero, values)))

def border_cell_ids_from_cells_per_vertices(values: list) -> list:
    """Return cell ids that are on boundary"""
    return list(map(mpas_indices, filter(lt_one, enumerate(values))))


class MpasGrid():
    """ MPAS Grid class
    """
    def __init__(self, filename: str=""):
        self._filename = filename
        self._dataset = None
        self._ncells = 0
        self._nvertices = 0
        self._nedges = 0
        self._edges_per_vertices:List[float] = []
        self._edge_cells = None
        self._border_cell_ids:List[int] = []
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
            self._cell_edges_per_vertices()
        else:
            print("Warning: Could not file")

    def _read_ncells(self):
        """Read the number of Cells in grid"""
        self._ncells = self._dataset.dimensions['nCells'].size

    @property
    def ncells(self):
        """Return number of cells in regional grid."""
        return self._ncells

    def _read_nvertices(self):
        """Read the number of Vertices in the grid"""
        self._nvertices = self._dataset.dimensions['nVertices'].size

    @property
    def nvertices(self):
        """Return number of vertices in regional grid."""
        return self._nvertices

    def _read_nedges(self):
        """Read the number of edges in the grid"""
        self._nedges = self._dataset.dimensions['nEdges'].size

    @property
    def nedges(self):
        """Return number of edges in regional grid."""
        return self._nedges

    def _cell_edges_per_vertices(self):
        """Returns a list of ratio of number of edges to vertices for each cell
        """
        for cell_id in range(self._ncells):
            n_cells_on_cell = len_non_zero(self._dataset.variables["cellsOnCell"][cell_id])
            n_vertices_on_cell = len_non_zero(self._dataset.variables["verticesOnCell"][cell_id])
            self._edges_per_vertices.append(n_cells_on_cell/n_vertices_on_cell)
        self._border_cell_ids = list(border_cell_ids_from_cells_per_vertices(self._edges_per_vertices))

    @property
    def border_cell_ids(self)->list:
        """Return edge cells in regional grid.
        """
        return self._border_cell_ids
