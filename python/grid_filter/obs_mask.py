'''
Helper functions to filter observation files.
'''
import numpy as np
import h5py

def filter_obs_by_mask(obs: np.ndarray, mask: np.ndarray)->np.ndarray:
    ''' Filter observations against mask.
    '''
    obs_dtype = type(obs[0])
    vfunc = np.vectorize(lambda x, m: x if m else 0)
    filtered_output = vfunc(obs, mask)
    filtered_output = filtered_output[filtered_output != 0]

    return filtered_output

