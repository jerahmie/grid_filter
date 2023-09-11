#!/usr/bin/env python3
'''
Generate random points 
'''
import sys
import os
import multiprocessing
import grid_filter as gf

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
   
    gf.filter_main(args.static_file, args.obs_file,
            args.lam_mask_file,
            multiprocessing.cpu_count())
