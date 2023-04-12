#!/usr/bin/env python3
"""
Plot the MPAS grid data on map.
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from grid_perimeter import MpasGrid, get_mpas_grid, get_grid_lat_lon, plot_mpas_grid, overplot_mpas_grid

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="MPAS grid data NetCDF file.")
    args = parser.parse_args()

    if not os.path.exists(args.filename):
        err_txt = "Could not find NetCDF file: {filename}"
        sys.exit(err_txt.format(filename=args.filename))

    mpg = MpasGrid(args.filename)
    border_cell_ids = mpg.border_cell_ids

    cell_lat, cell_lon = get_mpas_grid(args.filename)
    perim_cell_lat, perim_cell_lon = get_grid_lat_lon(args.filename, border_cell_ids)
    ax = plot_mpas_grid(cell_lat, cell_lon)
    print("Saving region grid plot.")
    plt.savefig('regional_grid.png')
    overplot_mpas_grid(ax, perim_cell_lat, perim_cell_lon)
    print("Saving regional grid plot with perimeter.")
    plt.savefig('regional_grid_perimeter.png')

   
    print("Done.")
