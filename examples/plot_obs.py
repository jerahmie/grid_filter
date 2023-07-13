#!/usr/bin/env python3
""" Plot the non-filtered and filtered Dataset.
"""
import os
import sys
import errno
import argparse
import h5py 
#from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import grid_filter

def plot_obs(latc: np.ndarray, lonc: np.ndarray, mask: np.ndarray = None) -> plt.axes:
    """ Returns a matplotlib axes that 
    """
    nlats = np.size(latc)
    nlons = np.size(lonc)
    if (nlats != nlons):
        sys.exit(f'Number of latitude and longitude points must agree. ({nlats} != {nlons})') 
    if mask is not None :
        mask_id = np.nonzero(mask)
    else:
        mask = np.ones((nlats))
        mask_id = np.nonzero(mask)

    print(f'latc: {min(latc):.2f}, {max(latc):.2f}')
    print(f'lonc: {min(lonc):.2f}, {max(lonc):.2f}')
    print("Generating plot...")
    #proj = ccrs.Orthographic(central_longitude=270, central_latitude=45)
    proj = ccrs.PlateCarree(central_longitude=0.0)
    ax = plt.axes(projection=proj)
    ax.set_global()

    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.LAKES,
                   facecolor='gray',
                   edgecolor='black',
                   linewidth=0.5)
    ax.add_feature(cfeature.STATES,
                   facecolor='lightgray',
                   edgecolor='black',
                   linewidth=0.5)
    for i in mask_id:
        ax.plot(lonc[i], latc[i], color='blue', linestyle='None', marker='o', markersize=1, transform=ccrs.Geodetic())
    return ax
    
def overplot_points(ax: plt.axes, lats: np.ndarray, lons: np.ndarray, color="red") -> plt.axes:
    """Plot lats, lons over existing plt axes.

    Keyword arguments:
    ax -- matplotlib.pyplot axes 
    lats -- latitiude points
    lons -- longitude points
    color -- custom color 
    """
    print(f"[overplot_points] np.shape(lats): {np.shape(lats)}")
    print(f"[overplot_points] np.shape(lons): {np.shape(lons)}")
    if len(lats) != len(lons):
        sys.exit(f"Latitude {len(lats)} and Longitudes {len(lons)} not equal.")
    for i in range(len(lats)):
        ax.plot(lons[i], lats[i], color=color, linestyle='None', marker='o', markersize=1, transform=ccrs.Geodetic())

    return ax

def main(args)->None:
    """Plot Observations.
    """
    if not os.path.exists(args.filename):
        raise FileNotFoundError( errno.ENOENT, os.strerror(errno.ENOENT), args.filename)
    #filter_mask = grid_filter.read_h5data(args.filename, 'DerivedValue', 'LAMDomainCheck')
    latc = grid_filter.read_h5data(args.filename, 'MetaData', 'latitude')
    lonc = grid_filter.read_h5data(args.filename, 'MetaData', 'longitude')
    
    #ax = plot_obs(latc, lonc, filter_mask)
    ax = plot_obs(latc, lonc)
    print("Saving filtered observation points.")
    if args.static_file is not None:
        mpg = grid_filter.MPASGrid(args.static_file)
        pts = 180.0/np.pi*np.array(mpg.cell_points())
        print(f"np.shape(pts): {np.shape(pts)} type: {type(pts)}")
        overplot_points(ax, pts[:,0], pts[:,1])

    plt.savefig('plot_obs.png')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog='plot_obs',
                        description='Plot the filter observations.',
                        epilog='plot_obs')
    parser.add_argument('filename',
                        help="Observation file (HDF5)")
    parser.add_argument('--static_file',
                        help="Regional MPAS Grid file (NetCDF).",
                        required=False)
    args = parser.parse_args()
    main(args)
    #grid_filter.plot_mpas_grid(cell_lat, cell_lon)
