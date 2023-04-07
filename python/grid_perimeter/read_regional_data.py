"""
Read regional grid data.
"""
import os
import sys
import numpy as np
from netCDF4 import Dataset

def mpas_cells(nc: Dataset) -> (np.ndarray, np.ndarray):
    """ Return MPAS Cells
    """
    nCells = nc.dimensions['nCells'].size
    latCell = nc.variables['latCell']
    lonCell = nc.variables['lonCell']

    return np.array(latCell[:], dtype=float), np.array(lonCell[:], dtype=float)

def get_mpas_grid(filename: str) -> (np.ndarray, np.ndarray):
    """ Read netcdf regional array data 
    """
    grid_ds = Dataset(filename, 'r')
    nCells = grid_ds.dimensions['nCells'].size
    nEdges = grid_ds.dimensions['nEdges'].size
    nVertices = grid_ds.dimensions['nVertices'].size
    cell_lat, cell_lon = mpas_cells(grid_ds)
    return cell_lat, cell_lon

