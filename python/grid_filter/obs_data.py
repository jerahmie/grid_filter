"""
Helper functions to read and process observation points.
"""
import os
from typing import List
import numpy as np
import h5py

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
    """Return the observation points from dataset as a 2 by N numpy array.2 by N numpy array. 

    Keyword Arguments
    file_name: String representing valid path to hdf5 file
    """
    latc = read_h5data(file_name, 'MetaData', 'latitude')
    lonc = read_h5data(file_name, 'MetaData', 'longitude')
    return np.transpose(np.stack((latc, lonc)))


