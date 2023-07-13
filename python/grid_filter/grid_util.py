"""
grid perimeter caluculation 
"""
import os
from typing import List, Tuple

gt_zero = lambda x: x>0      # filter function for integers greater than zero
lt_one = lambda ix: ix[1]<1.0     # filter function for values under 1.0
mpas_indices = lambda ix: ix[0]   # index from enumerated tuple element

def len_non_zero(values: list) -> int:
    """Helper to find the number of non-zeros in a list"""
    return len(list(filter(gt_zero, values)))

def border_cell_ids_from_cells_per_vertices(values: list) -> list:
    """Return cell ids that are on boundary"""
    return list(map(mpas_indices, filter(lt_one, enumerate(values))))

def filter_bdy_mask_cell(ptsi, bdy_cell, cell_type) -> List[Tuple[float, float, int]]:
    """Filter list of points by boundary cell type.
    Keyword arguments
    ptsi -- list of indexed points: [(lat, lon, index), ...]
    bdy_cell -- list of bdyMaskCell
    cell_type -- bydyMaskCell types to filter
    """
    return zip(*filter(lambda x: True if x[1] in cell_type else False, zip(ptsi, bdy_cell)))

