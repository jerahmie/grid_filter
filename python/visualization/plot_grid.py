#!/usr/bin/env python3
"""
Plot the MPAS grid.
"""
import os
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def plot_mpas_grid(lats: np.ndarray, lons: np.ndarray) -> plt.figure:
    """ generate a matplotlib plot with grid overlay on map projection
    
    Keyword arguments: 
    grid_data 
    """
    print(type(lats))
    lats_deg = 180.0/np.pi*lats
    lons_deg = 180.0/np.pi*lons
    fig = plt.figure()
    proj = ccrs.Orthographic(central_longitude=270, central_latitude=45)
    #proj = ccrs.PlateCarree()
    ax = plt.axes(projection=proj)
    ax.set_global()

    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.LAKES,
                   facecolor='cyan',
                   edgecolor='black',
                   linewidth=0.5)
    ax.add_feature(cfeature.STATES,
                   facecolor='lightgray',
                   edgecolor='black',
                   linewidth=0.5)
    lons_min = np.min(lons_deg)
    lons_max = np.max(lons_deg)
    lats_min = np.min(lats_deg)
    lats_max = np.max(lats_deg)
    ax.set_extent([lons_min, lons_max, lats_min, lats_max])
    for i in range(len(lats)):
        ax.plot(lons_deg[i], lats_deg[i], color='black', marker='o', markersize=1, transform=ccrs.Geodetic())
    
    return ax

if __name__ == "__main__":
    print("Display MPAS grid...")

