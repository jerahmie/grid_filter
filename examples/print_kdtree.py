#!/usr/bin/env python
"""Print the KD-tree 
"""
import sys
import os
from grid_filter import MPASGrid, KDTree2D, KDTreeDisplay

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="MPAS grid data NetCDF file.")
    args = parser.parse_args()

    if not os.path.exists(args.filename):
        ERR_TXT = "Could not find NetCDF file: {filename}"
        sys.exit(ERR_TXT.format(filename=args.filename))

    mpg = MPASGrid(args.filename)
    pts = mpg.cell_points()
    ptsi = [(pts[i][0], pts[i][1], i) for i in range(len(pts))]
    kd2 = KDTree2D(ptsi)
    kd_display = KDTreeDisplay(kd2)
    #print(kd_display.tree_list)
    print('')
    print('-----------------------------------------')
    kd_display.find_path(440)
    print('-----------------------------------------')
    kd_display.find_path(268)
    #for node in path_to_point:
    #    print(node)
     
