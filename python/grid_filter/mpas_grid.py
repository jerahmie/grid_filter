'''
file - mpas_grid.py
Class read and store Regional MPAS grid data in a class.
'''
import os
from netCDF4 import Dataset
from typing import List, Tuple
from .grid_util import len_non_zero, border_cell_ids_from_cells_per_vertices

class MPASGrid():
    """ MPAS Grid class
    """
    def __init__(self, filename: str=""):
        self._filename = filename
        self._ncells = 0
        self._nvertices = 0
        self._nedges = 0
        self._edges_per_vertices: List[float] = []
        self._edge_cells = None
        self._border_cell_ids: List[int] = []
        self._cell_lat: List[float] = []
        self._cell_lon: List[float] = []
        self._bdy_mask_cell: List[float] = []
        if os.path.exists(filename):
            self._load_dataset()

    def _load_dataset(self):
        """Loads grid data from netCDF4 file
        """
        if os.path.exists(self._filename):
            with Dataset(self._filename, 'r') as ds:
                self._read_ncells(ds)
                self._read_nvertices(ds)
                self._read_nedges(ds)
                self._cell_edges_per_vertices(ds)
                self._read_cell_lat_lon(ds)
                self._read_bdy_mask_cell(ds)
        else:
            print("Warning: Could not file")

    def _read_ncells(self, ds: Dataset) -> None:
        """Read the number of Cells in grid"""
        self._ncells = ds.dimensions['nCells'].size

    def _read_cell_lat_lon(self, ds: Dataset) -> None:
        """Read the latitude and longitude values of cells in mesh"""
        for cell_id in range(self._ncells):
            self._cell_lat.append(float(ds.variables['latCell'][cell_id]))
            self._cell_lon.append(float(ds.variables['lonCell'][cell_id]))

    def _read_bdy_mask_cell(self, ds: Dataset) -> None:
        """Read the cell type""" 
        for cell_id in range(self._ncells):
            self._bdy_mask_cell.append(int(ds.variables['bdyMaskCell'][cell_id]))

    @property
    def ncells(self):
        """Return number of cells in regional grid."""
        return self._ncells

    def _read_nvertices(self, ds: Dataset) -> None:
        """Read the number of Vertices in the grid"""
        self._nvertices = ds.dimensions['nVertices'].size

    @property
    def nvertices(self) -> None:
        """Return number of vertices in regional grid."""
        return self._nvertices

    def _read_nedges(self, ds: Dataset) -> None:
        """Read the number of edges in the grid"""
        self._nedges = ds.dimensions['nEdges'].size

    @property
    def nedges(self):
        """Return number of edges in regional grid."""
        return self._nedges

    def _cell_edges_per_vertices(self, ds):
        """Returns a list of ratio of number of edges to vertices for each cell
        """
        for cell_id in range(self._ncells):
            n_cells_on_cell = len_non_zero(ds.variables["cellsOnCell"][cell_id])
            n_vertices_on_cell = len_non_zero(ds.variables["verticesOnCell"][cell_id])
            self._edges_per_vertices.append(n_cells_on_cell/n_vertices_on_cell)
        self._border_cell_ids = \
                list(border_cell_ids_from_cells_per_vertices(self._edges_per_vertices))

    @property
    def border_cell_ids(self)->List[int]:
        """Return edge cells in regional grid.
        """
        return self._border_cell_ids
   
    @property
    def bdy_mask_cells(self)->List[int]:
        """Return the boundary mask cells.
        """
        return self._bdy_mask_cell

    def cell_points(self)->List[Tuple[float, float, int]]:
        """Return cell zipped list of cell points. Index order is same as grid mesh."""
        cell_points = zip(self._cell_lat, self._cell_lon)
        return list(cell_points)
