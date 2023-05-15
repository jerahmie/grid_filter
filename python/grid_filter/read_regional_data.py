"""
Read regional grid data.
"""
from typing import Tuple
import numpy as np
from netCDF4 import Dataset

def mpas_cells(nc: Dataset) -> Tuple[np.ndarray, np.ndarray]:
    """ Return MPAS Cells
    """
    lat_cell = nc.variables['latCell']
    lon_cell = nc.variables['lonCell']

    return np.array(lat_cell[:], dtype=float), np.array(lon_cell[:], dtype=float)

def get_mpas_grid(filename: str) -> Tuple[np.ndarray, np.ndarray]:
    """ Read netcdf regional array data 
    """
    with Dataset(filename, 'r') as grid_ds:
        nCells = grid_ds.dimensions['nCells'].size
        nEdges = grid_ds.dimensions['nEdges'].size
        nVertices = grid_ds.dimensions['nVertices'].size
        cell_lat, cell_lon = mpas_cells(grid_ds)

    return cell_lat, cell_lon

def get_grid_lat_lon(filename: str, cell_ids: list) -> Tuple[np.ndarray, np.ndarray]:
    """Get lats, lons of list of grid indices"""
    with Dataset(filename, 'r') as grid_ds:
        cell_lat = []
        cell_lon = []
        for cell_id in cell_ids:
            cell_lat.append(grid_ds.variables['latCell'][cell_id])
            cell_lon.append(grid_ds.variables['lonCell'][cell_id])

    return np.array(cell_lat, dtype=float), np.array(cell_lon, dtype=float)
