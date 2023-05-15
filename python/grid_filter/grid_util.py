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