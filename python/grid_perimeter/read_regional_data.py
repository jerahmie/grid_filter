#!/usr/bin/env python3
"""
Read regional grid data.
"""
import os
import sys
import numpy as np
from netCDF4 import Dataset

def get_mesh_data(filename: str) -> np.ndarray:
    """
    get_mesh_data
    Read netcdf regional array data 
    """
    print(os.path.exists(filename))
    return np.zeros(10)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="regional grid data NetCDF file.")
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        err_txt = "Could not find NetCDF file: {filename}"
        sys.exit(err_txt.format(filename=args.filename))
    get_mesh_data(args.filename)
    print("Done.")
