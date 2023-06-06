#!/usr/bin/env python3
"""
Plot the MPAS grid.
"""
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


def pad_max(x, p):
    """Pad maximum latitude/longitude region"""
    if x > 0.0:
        return (1.0+p)*x
    else:
        return (1.0-p)*x

def pad_min(x, p):
    """Pad minimum latitude/longitude region"""
    if x > 0.0:
        return (1.0-p)*x
    else:
        return (1.0+p)*x

def plot_mpas_grid(lats: np.ndarray, lons: np.ndarray) -> plt.axes:
    """ generate a matplotlib plot with grid overlay on map projection
    Keyword arguments: 
    lats -- 1D (nCells) numpy array of latitudes (radians)
    lons -- 1D (nCells) numpy array of longitudes (radians)
    """
    print("Plotting interior mesh cell lats/lons")
    lats_deg = 180.0/np.pi*lats
    lons_deg = 180.0/np.pi*lons
    plt.figure()
    proj = ccrs.Orthographic(central_longitude=270, central_latitude=45)
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

    lons_min = pad_min(np.min(lons_deg), 0.01)
    lons_max = pad_max(np.max(lons_deg), 0.01)
    lats_min = pad_min(np.min(lats_deg), 0.05)
    lats_max = pad_max(np.max(lats_deg), 0.05)
    ax.set_extent([lons_min, lons_max, lats_min, lats_max])
    for i in range(len(lats)):
        ax.plot(lons_deg[i], lats_deg[i], color='gray', marker='o',
                markersize=1, transform=ccrs.Geodetic())

    return ax

def overplot_mpas_grid(ax: plt.axes, lats: np.ndarray, lons: np.ndarray, color="red") -> None:
    """Plot points over an existing matplotlib axes.
    
    Keyword arguments:
    ax   --  matplot lib axes to be modified
    lats --  1D (N) numpy array of latitudes (radians)
    lons --  1D (N) numpy array of longitudes (radians)
    """
    print("Plotting perimeter lats and lons.")
    lats_deg = 180.0/np.pi * lats
    lons_deg = 180.0/np.pi * lons
    for i in range(len(lats)):
        ax.plot(lons_deg[i], lats_deg[i], color=color, marker='o',
                markersize=2, linestyle='solid', linewidth=2, transform=ccrs.Geodetic())

if __name__ == "__main__":
    print("Display MPAS grid...")
