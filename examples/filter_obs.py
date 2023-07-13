#!/usr/bin/env python3
"""
Generate random points 
"""
import os
import sys
import time
from typing import List, Tuple
from random import uniform
import numpy as np
import matplotlib.pyplot as plt
import h5py
import grid_filter as gf
from grid_filter import KDTree2D, Node2D, MPASGrid

def grid_filter(kd2d: KDTree2D, bdy_cells: np.ndarray, obs: np.ndarray) -> np.ndarray:
    """ grid_filter: generate observation point mask.

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

def save_data(filename: str, grp_name: str, dset_name: str, dset: np.ndarray) -> None:
    """Save the dataset to a hdf5 file.

    Keyword arguments
    filename --
    grp_name --
    dset_name --
    """
    fh = h5py.File(filename, 'w') 
    if grp_name != '':
        grp = fh.create_group('/'+grp_name)
    else:
        grp = fh.get('/')
    grp.create_dataset(dset_name, data=dset) 
    fh.close()        

def main(static_file: str, obs_file: str, save_file: str) -> None:
    """Construct KDTree, load observation points, and save mask to data
    """
    print("Read Grid")
    t1 = time.time()
    mpg = MPASGrid(static_file)
    t2 = time.time()
    print(f"read mpas_grid: {t2-t1:.2f}")
    # cell grid points (lat, lon)
    pts = mpg.cell_points()
    bdy_msk = mpg.bdy_mask_cells
    t3 = time.time()
    print(f"prepare cell_points: {t2-t1:.2f}")
    
    print('Build KDTree2D')
    # cell grid points with index (lat, lon, i)
    ptsi = [(180.0/np.pi*pts[i][0], 180.0/np.pi*pts[i][1], i) for i in range(len(pts))]
    ptsi_filtered, _ = gf.filter_bdy_mask_cell(ptsi, bdy_msk, {6,7})
    kd2d = KDTree2D(ptsi_filtered)
    t4 = time.time()
    print(f"build kdtree: {t3-t2:.2f}")

    # read observation points
    obs_pts = gf.obs_points(obs_file)
    t5 = time.time()
    print(f"read obs_points: {t5-t4:.2f}")

    mask = grid_filter(kd2d, bdy_msk, obs_pts)
    t6 = time.time()
    print(f"filter obs: {t6-t5:.2f}")

    # save mask data
    print('Saving Data')
    save_data(save_file, 'DerivedValue', 'LAMDomainCheck', mask)
    t7 = time.time()
    print(f"save_data: {t7-t6:.2f}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("static_file", help="MPAS regional static file (NetCDF).")
    parser.add_argument("obs_file", help="Observation file (HDF5).")
    parser.add_argument("save_file", help="Output mask save file (HDF5).", default='lam_mask.h5')
    args = parser.parse_args()

    if not os.path.exists(args.static_file):
        ERR_TXT = "Could not find NetCDF file: {filename}"
        sys.exit(ERR_TXT.format(filename=args.static_file))
    
    if not os.path.exists(args.obs_file):
        ERR_TXT = "Could not find HDF5 file: {filename}"
        sys.exit(ERR_TXT.format(filename=args.obs_file))
   
    main(args.static_file, args.obs_file, args.save_file)
