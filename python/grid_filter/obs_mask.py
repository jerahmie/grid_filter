'''
Helper functions to filter observation files.
'''
import numpy as np
import h5py

def filter_obs_by_mask(obs: np.ndarray, mask: np.ndarray)->np.ndarray:
    ''' Filter observations against mask.
    '''
    filtered_output_reduced = []
    for i,m in enumerate(mask):
        if m :
            filtered_output_reduced.append(obs[i])

    return np.array(filtered_output_reduced, dtype=obs.dtype)

