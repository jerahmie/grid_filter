"""
grid_filter: LAM Domain observation filter routines.
"""
import numpy as np
from grid_filter import KDTree2D

def lam_domain_filter(kd2d: KDTree2D, bdy_cells: np.ndarray, obs: np.ndarray) -> np.ndarray:
    """ lam_domain_filter: generate observation point mask.

    Keyword arguments:
    kd2d -- 2D KDTree
    obs  -- Numpy observation array.
    """
    mask = np.zeros(np.shape(obs)[0],dtype=int)
    print(f"[grid_filter] len(bdy_cells): {len(bdy_cells)}")
    for i, pt in enumerate(obs):
        if i%1000 == 0:
            print(f"[grid_filter] {i}")
        cell_id =  kd2d.nearest_cell(pt)
        cell_type = bdy_cells[cell_id]
        if cell_type < 7:
            mask[i] = 1

    return mask
