"""
Helper functions to read and process observation points.
"""
import numpy as np
import h5py
from .kdtree import KDTree2D

def read_h5data(filename: str, group: str, dataset: str)->np.ndarray:
    """ Return the filtered mask as a numpy ndarray.

    Keyword Arguments:
    filename - string containing file path of hdf5 file
    group - group name in hdf5 file
    dataset - dataset name
    """
    with h5py.File(filename, 'r') as fobs:
        dset = fobs[f'/{group}/{dataset}'][:]
    return dset


def obs_points(file_name: str) -> np.ndarray:
    """Return the observation points from dataset as a 2 by N numpy array."

    Keyword Arguments
    file_name: String representing valid path to hdf5 file
    """
    latc = read_h5data(file_name, 'MetaData', 'latitude')
    lonc = read_h5data(file_name, 'MetaData', 'longitude')
    lonc[np.argwhere(lonc<0.0)] += 360.0
    return np.transpose(np.stack((latc, lonc)))

def gen_obs_mask(kd2d: KDTree2D, bdy_cells: np.ndarray, obs: np.ndarray) -> np.ndarray:
    """ gen_obs_mask: generate observation point mask.

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
def save_obs_data(filename: str, grp_name: str, dset_name: str, \
                dset: np.ndarray, mode: str='w') -> None:
    '''Save the dataset to a hdf5 file.
    Keyword arguments
    filename -- output file name string
    grp_name -- HDF5 group name
    dset_name -- HDF5 dataset name
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


