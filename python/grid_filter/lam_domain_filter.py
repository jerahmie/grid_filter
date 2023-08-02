'''
grid_filter: LAM Domain observation filter routines.
'''
from typing import Tuple
import numpy as np
from grid_filter import KDTree2D

def lam_domain_filter(kd2d: KDTree2D, bdy_cells: np.ndarray, obs: np.ndarray, \
        min_max:Tuple[Tuple[float, float], Tuple[float, float]]=None) \
        -> Tuple[np.ndarray, np.ndarray]:
    ''' lam_domain_filter: generate observation point mask.

    Keyword arguments:
    kd2d -- 2D KDTree
    obs  -- Numpy observation array.
    prefilter -- enable prefiltering
    '''
    if min_max:
        prefilter = True
        min_lat = min_max[0][0]
        max_lat = min_max[0][1]
        min_lon = min_max[1][0]
        max_lon = min_max[1][1]
    else:
        prefilter = False
        min_lat = 0.0
        max_lat = 0.0
        min_lon = 0.0
        max_lon = 0.0

    mask = np.zeros(np.shape(obs)[0], dtype=int)
    ncompares = np.zeros(np.shape(obs)[0], dtype=int)
    print(f'[lam_domain_filter] len(bdy_cells): {len(bdy_cells)}')
    for i, pt in enumerate(obs):
        if i%1000 == 0:
            print(f'[grid_filter] {i}')
        if prefilter and ((min_lat >= pt[0]) or (max_lat <= pt[0]) \
                and (min_lon >= pt[1]) or (max_lon <= pt[1])):
            pass
        else:
            cell_id =  kd2d.nearest_cell(pt)
            cell_type = bdy_cells[cell_id]
            ncompares[i] = kd2d.compares
            if cell_type < 7:
                mask[i] = 1

    return mask, ncompares
