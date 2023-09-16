"""
Helper functions to read and process observation points.
"""
import numpy as np
import h5py
from .kdtree import KDTree2D
from .obs_mask import filter_obs_by_mask

H5_DATASET_TYPE = h5py._hl.dataset.Dataset
H5_GROUP_TYPE = h5py._hl.group.Group

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

def dfs(fh:h5py._hl.files.File, data_paths:list, path:str='/') -> None:
    '''Depth-first search of hdf5 file dataset paths.
    Keyword arguments
    fh         -- file handle of open hdf5 file.
    data_paths -- list of file paths, filled recursively, depth-first
    path       -- current path in hdf5 file.

    '''
    keys = list(fh[path].keys())
    for key in keys:
        new_path  = path + '/' + key    # next path to check in hdf5 file
        if type(fh[new_path]) == H5_DATASET_TYPE:
            data_paths.append(fh[new_path].name)
        elif type(fh[new_path]) == H5_GROUP_TYPE:
            dfs(fh, data_paths, new_path)
        else:
            raise(ValueError("HDF5 file path unknown type."))


def save_ioda_filtered(mask: np.ndarray, obsfile: str, obsfile_filtered: str) -> None:
    '''Apply filter to data in ioda observation file. Save data to obsfile_filtered.
    
    Keyword arguments
    mask    -- mask file for regional domain
    obsfile -- ioda format hdf5 obsvation file.
    obsfile_filtered -- output ioda format hdf5 file filtered against mask.
    '''
    try: 
        fh = h5py.File(obsfile, 'r')
    except IOError as e:
        print(f'Observation file {obsfile} could not be opened.')
        raise e
    try:
        fhout = h5py.File(obsfile_filtered, 'w')
    except IOError as e:
        print(f'Output file {obsfile_filtered} could not be opened.')
        raise e
    
    # copy global attributes
    attrs = fh.attrs
    for attr in attrs:
        fhout['/'].attrs[attr] = fh['/'].attrs[attr]

    # find all datapaths
    data_paths = []
    dfs(fh, data_paths)

    # create groups group structure
    for path in data_paths:
        groups = path.split('/')[1:-1]
        current_path = ''
        for group in groups:
            current_path += '/' + group
            if not group in list(fhout.keys()):
                fhout.create_group(current_path)

    # create and populate datasets
    for path in data_paths:
        dset_data = fh[path][:]
        if len(dset_data) == len(mask):
            dset_filtered = filter_obs_by_mask(dset_data, mask)
            dset = fhout.create_dataset(path, data=dset_filtered)
        else:
            dset = fhout.create_dataset(path, data=dset_data)
        # update dataset attributes
        for attr in fh[path].attrs:
            dset.attrs[attr] = attr
    
    fhout.close()
    fh.close()
