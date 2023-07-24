#!/usr/bin/env python3
'''
Generate random points 
'''
import os
import sys
import time
from collections import namedtuple
from multiprocessing import shared_memory
import multiprocessing
from concurrent.futures.process import ProcessPoolExecutor
import numpy as np
import h5py
import grid_filter as gf
from grid_filter import KDTree2D, MPASGrid

Obsinfo = namedtuple('Obsinfo', 'shape data_type')

def save_data(filename: str, grp_name: str, dset_name: str, dset: np.ndarray, mode: str='w') -> None:
    '''Save the dataset to a hdf5 file.
    Keyword arguments
    filename --
    grp_name --
    dset_name --
    mode -- h5py mode (default='w')
    '''
    if mode not in ['w', 'a']: 
        raise Exception('Invalid h5py write mode.')

    fh = h5py.File(filename, mode) 
    if grp_name != '':
        grp = fh.create_group('/'+grp_name)
    else:
        grp = fh.get('/')
    grp.create_dataset(dset_name, data=dset) 
    fh.close()

def create_shared_memory(data:np.ndarray, shared_name:str) -> shared_memory.SharedMemory:
    '''Create shared memory block for multiprocessing.
    '''
    data_shape = np.shape(data)
    data_type = data.dtype
    d_size = np.dtype(data_type).itemsize * np.prod(data_shape)
    print(f"data_shape: {data_shape}, data_type: {data_type}, d_size: {d_size}")
    shm = shared_memory.SharedMemory(create=True, size=d_size, name=shared_name)
    dst = np.ndarray(shape=data_shape, dtype=data_type, buffer=shm.buf)
    dst[:] = data[:]
    return shm

def release_shared(name:str) -> None:
    '''Free shared memory block
    '''
    shm = shared_memory.SharedMemory(name=name)
    shm.close()
    shm.unlink()

def lam_domain_filter_mp(shm_name, mask_shm_name, kd2d, bdy_msk, start, stop, obsinfo):
    '''Filter subset of observations.
    Keyword arguments:
    shm_name -- Observation data, shared memory region visible to all processes
    mask_shm_name -- Mask data, shared memory region, visible to all processes
    kd2d -- 2D kdtree of MPAS regional domain
    bdy_msk -- boundary mask cells types
    start -- start index
    stop -- stop index
    obsinfo -- tuple containing shared memory size, data type
    '''
    shm = shared_memory.SharedMemory(name=shm_name)
    mask_shm = shared_memory.SharedMemory(name=mask_shm_name)
    obs_pts = np.ndarray(obsinfo.shape, dtype=obsinfo.data_type, buffer=shm.buf)
    mask = np.ndarray(obsinfo.shape[0], dtype=int, buffer=mask_shm.buf)
    print(f'start: {start}, stop: {stop}')
    #obs_pts[start:stop][:] = float(start)
    mask[start:stop] = gf.lam_domain_filter(kd2d, bdy_msk, obs_pts[start:stop])

def main(static_file: str, obs_file: str, save_file: str, nproc: int=1) -> None:
    '''Construct KDTree, load observation points, and save mask to data
    Keyword arguments:
    static_file --
    obs_file --
    save_file -- 
    nproc -- Number of processes
    '''
    print('Read Grid')
    t1 = time.time()
    mpg = MPASGrid(static_file)
    t2 = time.time()
    t_read_mpas_grid = t2 - t1
    print(f'read mpas_grid: {t_read_mpas_grid:.2f}')
    # cell grid points (lat, lon)
    pts = mpg.cell_points()
    bdy_msk = mpg.bdy_mask_cells
    t3 = time.time()
    print(f'prepare cell_points: {t3-t2:.2f}')
    
    print('Build KDTree2D')
    # cell grid points with index (lat, lon, i)
    ptsi = [(180.0/np.pi*pts[i][0], 180.0/np.pi*pts[i][1], i) for i in range(len(pts))]
    ptsi_filtered, _ = gf.filter_bdy_mask_cell(ptsi, bdy_msk, {6,7})
    kd2d = KDTree2D(ptsi_filtered)
    
    t4 = time.time()
    t_build_kdtree = t4-t3
    print(f'build kdtree: {t_build_kdtree:.2f}')

    # read observation points
    obs_pts = gf.obs_points(obs_file)

    t5 = time.time()
    t_read_obs = t5 - t4
    print(f'read obs_points: {t_read_obs:.2f}')

    print('setup multiprocessing')
    #futures = []
    obs_share_name = 'obs_pts'
    create_shared_memory(obs_pts, obs_share_name)

    t6 = time.time()
    print(f'filter obs: {t6-t5:.2f}')

    nobs = np.shape(obs_pts)[0]
    chunk_size = int(nobs/nproc)
    obsinfo = Obsinfo(np.shape(obs_pts), type(obs_pts[0][0]))

    # allocate mask space
    mask_share_name = 'mask_pts'
    mask = np.zeros(nobs, dtype=int)
    mask_shm = create_shared_memory(mask, mask_share_name)

    print(f'shape obs_shm: {np.shape(obs_pts)}, {obs_pts[0]}, ' + \
           'chunk_size: {chunk_size}') 
    with ProcessPoolExecutor(max_workers=nproc) as executor:
        for i in range(0, nproc):
            start = i*chunk_size
            print(f'start: {start}')
            executor.submit(lam_domain_filter_mp, obs_share_name,
                            mask_share_name, kd2d, bdy_msk, start,
                            start+chunk_size, obsinfo)

    mask_out = np.ndarray(np.shape(mask), dtype=type(mask[0]), buffer=mask_shm.buf)
    t7 = time.time()
    t_obs_filter = t7-t5
    print(f'shape: {np.shape(mask_out)}, sum: {np.sum(mask_out)}')
    print(f'filter data: {t_obs_filter:.2f}') 
    release_shared(obs_share_name)
    # save mask data
    print('Saving Data')
    save_data(save_file, 'DerivedValue', 'LAMDomainCheck', mask_out)
    release_shared(mask_share_name)
    t8 = time.time()
    t_save_mask = t8-t7
    print(f'save_data: {t_save_mask:.2f}')
    print('')
    print('              === Timing Summary===')
    print(f'MPAS Regional Domain Cells .. {len(pts)}')
    print(f'    Number of Observations .. {nobs}')
    print(f'     Read MPAS Static File .. {t_read_mpas_grid:.2f} sec')
    print(f'         Read Observations .. {t_read_obs:.2f} sec')
    print(f'          Construct KDTree .. {t_build_kdtree:.2f} sec')
    print(f'       Filter Observations .. {t_obs_filter:.2f} sec')
    print(f'                 Save Mask .. {t_save_mask:.2f} sec')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
                        prog='filter_obs',
                        description='Generate limited area model mask for a set of ' + \
                                'observations within a Regional MPAS domain.',
                        epilog='EXAMPLE\n\t$./filter_obs.py conus_15km.static.nc ' + \
                               'satwind_obs.h5 obsmask.h5\n')
    parser.add_argument('static_file',
                        help='MPAS regional static file (NetCDF).')
    parser.add_argument('obs_file',
                        help='Observation file (HDF5).')
    parser.add_argument('lam_mask_file',
                        help='Output mask save file (HDF5).',
                        default='lam_mask.h5')
    args = parser.parse_args()

    if not os.path.exists(args.static_file):
        ERR_TXT = 'Could not find NetCDF file: {filename}'
        sys.exit(ERR_TXT.format(filename=args.static_file))
    
    if not os.path.exists(args.obs_file):
        ERR_TXT = 'Could not find HDF5 file: {filename}'
        sys.exit(ERR_TXT.format(filename=args.obs_file))
   
    main(args.static_file, args.obs_file,
            args.lam_mask_file,
            multiprocessing.cpu_count())
