#!/usr/bin/env python3
"""
Plot the MPAS grid data on map.
"""
import os
import sys
import matplotlib.pyplot as plt
import grid_filter as gf

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="MPAS grid data NetCDF file.")
    args = parser.parse_args()

    if not os.path.exists(args.filename):
        ERR_TXT = "Could not find NetCDF file: {filename}"
        sys.exit(ERR_TXT.format(filename=args.filename))

    mpg = gf.MPASGrid(args.filename)
    border_cell_ids = mpg.border_cell_ids
    cell_lat, cell_lon = gf.get_mpas_grid(args.filename)
    perim_cell_lat, perim_cell_lon = gf.get_grid_lat_lon(args.filename,
                                                          border_cell_ids)
    print('max_lat: ', max(perim_cell_lat))
    print('min_lat: ', min(perim_cell_lat))
    print('max_lon: ', max(perim_cell_lon))
    print('min_lat: ', min(perim_cell_lon))

    ax = gf.plot_mpas_grid(cell_lat, cell_lon)
    print("Saving region grid plot.")
    plt.savefig('regional_grid.png')
    gf.overplot_mpas_grid(ax, perim_cell_lat, perim_cell_lon)
    print("Saving regional grid plot with perimeter.")
    plt.savefig('regional_grid_perimeter.png')
    print("Done.")
