'''
file - lam_domain_filter.py
Filter all observations by finding nearest point in KDTree. If nearest point is internal to the MPAS Regional Domain, the binary mask of observations is set.
'''
import time
from typing import Tuple
from collections import namedtuple
import numpy as np
from multiprocessing import shared_memory
import multiprocessing
from concurrent.futures.process import ProcessPoolExecutor
import grid_filter as gf
from grid_filter import MPASGrid, KDTree2D

Obsinfo = namedtuple('Obsinfo', 'shape data_type')

def create_shared_memory(data:np.ndarray, \
        shared_name:str) -> shared_memory.SharedMemory:
    '''Create shared memory block for multiprocessing.
    '''
    data_shape = np.shape(data)
    data_type = data.dtype
    d_size = np.dtype(data_type).itemsize * np.prod(data_shape)
    print(f'data_shape: {data_shape},data_type: {data_type},d_size: {d_size}')
    shm = shared_memory.SharedMemory(create=True,size=d_size,name=shared_name)
    dst = np.ndarray(shape=data_shape, dtype=data_type, buffer=shm.buf)
    dst[:] = data[:]
    return shm

def release_shared(name:str) -> None:
    '''Free shared memory block
    '''
    shm = shared_memory.SharedMemory(name=name)
    shm.close()
    shm.unlink()

def lam_domain_filter_mp(shm_name, mask_shm_name, kd2d, bdy_msk, start, stop, obsinfo, min_max=None, stats_shm_name=None):
    '''Call lam_domain_filter using subset of observations divided across multiple
       processors.
    Keyword arguments:
    shm_name -- Observation data, shared memory region visible to all processes
    mask_shm_name -- Mask data, shared memory region, visible to all processes
    kd2d -- 2D kdtree of MPAS regional domain
    bdy_msk -- boundary mask cells types
    start -- start index
    stop -- stop index
    obsinfo -- tuple containing shared memory size, data type
    min_max -- prefilter lat/lon range ((min_lat, max_lat), (min_lon, max_lon)
    stats_shm_name -- search statistics shared mem name (optional)
    '''
    shm = shared_memory.SharedMemory(name=shm_name)
    mask_shm = shared_memory.SharedMemory(name=mask_shm_name)
    obs_pts = np.ndarray(obsinfo.shape, dtype=obsinfo.data_type, buffer=shm.buf)
    mask = np.ndarray(obsinfo.shape[0], dtype=int, buffer=mask_shm.buf)
    if stats_shm_name is not None:
        stats_shm = shared_memory.SharedMemory(name=stats_shm_name)
        stats = np.ndarray(obsinfo.shape[0], dtype=int, buffer=stats_shm.buf)
    else:
        stats = np.ndarray(stop-start+1, dtype=int)
    mask[start:stop], stats[start:stop] = \
            lam_domain_filter(kd2d, bdy_msk, obs_pts[start:stop], min_max)


def lam_domain_filter(kd2d:KDTree2D, bdy_cells: np.ndarray, obs: np.ndarray, \
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
        #if i%1000 == 0:
        #    print(f'[grid_filter] {i}')
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

def filter_main(static_file: str, obs_file: str, nproc: int=1) -> np.ndarray:
    '''Construct KDTree, load observation points, and save mask to data
    Keyword arguments:
    static_file -- MPAS regional domain static file (NetCDF)
    obs_file -- Observations input file name (HDF5)
    save_file -- Output file name (HDF5)
    nproc -- Number of processes
    '''
    print(f'Read Grid: {static_file}')
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

    min_max = gf.find_tree_min_max(kd2d.root)
    t4 = time.time()
    t_build_kdtree = t4-t3
    print(f'build kdtree: {t_build_kdtree:.2f}')

    # read observation points
    obs_pts = gf.obs_points(obs_file)

    t5 = time.time()
    t_read_obs = t5 - t4
    print(f'read obs_points: {t_read_obs:.2f}')

    print('setup multiprocessing')
    obs_share_name = 'obs_pts'
    gf.create_shared_memory(obs_pts, obs_share_name)

    t6 = time.time()
    print(f'filter obs: {t6-t5:.2f}')

    nobs = np.shape(obs_pts)[0]
    chunk_size = int(nobs/nproc)
    obsinfo = Obsinfo(np.shape(obs_pts), type(obs_pts[0][0]))

    # allocate mask space
    mask_share_name = 'mask_pts'
    mask = np.zeros(nobs, dtype=int)
    mask_shm = gf.create_shared_memory(mask, mask_share_name)

    # allocate space for search statistics (ex. number of compares)
    stats_share_name = 'stats_pts'
    stats = np.zeros(nobs, dtype=int)
    stats_shm = gf.create_shared_memory(stats, stats_share_name)

    print(f'shape obs_shm: {np.shape(obs_pts)}, {obs_pts[0]}, ' + \
           'chunk_size: {chunk_size}')
    with ProcessPoolExecutor(max_workers=nproc) as executor:
        for i in range(0, nproc):
            start = i*chunk_size
            print(f'start: {start}')
            executor.submit(gf.lam_domain_filter_mp, obs_share_name,
                            mask_share_name, kd2d, bdy_msk, start,
                            start+chunk_size, obsinfo, min_max, stats_share_name)
    mask_obs_sh = np.ndarray(np.shape(mask), dtype=type(mask[0]), buffer=mask_shm.buf)
    mask_out = np.copy(mask_obs_sh)

    ncompares = np.ndarray(np.shape(stats), dtype=type(stats[0]), buffer=stats_shm.buf)
    t7 = time.time()
    t_obs_filter = t7-t5
    print(f'shape: {np.shape(mask_obs_sh)}, sum: {np.sum(mask_obs_sh)}')
    print(f'filter data: {t_obs_filter:.2f}')
    gf.release_shared(obs_share_name)
    # save mask data
    print('Saving Data')
    #gf.save_obs_data(save_file, 'DerivedValue', 'LAMDomainCheck', mask_out, 'w')
    gf.release_shared(mask_share_name)
    #gf.save_obs_data(save_file, 'Statistics', 'ncompares', ncompares, 'a')
    gf.release_shared(stats_share_name)
    t8 = time.time()
    t_save_mask = t8-t7
    print(f'save_data: {t_save_mask:.2f}')
    print('')
    print('              === Timing Summary===')
    print(f'MPAS Regional Domain Cells .. {len(ptsi_filtered)}')
    print(f'    Number of Observations .. {nobs}')
    print(f'     Read MPAS Static File .. {t_read_mpas_grid:.2f} sec')
    print(f'         Read Observations .. {t_read_obs:.2f} sec')
    print(f'          Construct KDTree .. {t_build_kdtree:.2f} sec')
    print(f'       Filter Observations .. {t_obs_filter:.2f} sec')
    print(f'                 Save Mask .. {t_save_mask:.2f} sec')

    return mask_out

