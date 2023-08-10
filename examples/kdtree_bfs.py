#!/usr/bin/env python
"""Save Breadth-First Search of KDTree to file.
"""
import sys
import os
from typing import List
from grid_filter import MPASGrid, KDTree2D, KDTreeDisplay, Node2D


def traverse_bfs(kd2d : KDTree2D) -> List[Node2D]:
    """ Return a list of 2D nodes by traversing the KDTree 
    with a breadth-first search.

    Keyword arguments:
    kd2d -- 2D KDTree 
    """
    node_stack = []
    node_stack.append(kd2d)
    bfs = []
    while len(node_stack) > 0:
        curr_node = node_stack.pop(0)
        bfs.append(curr_node)
        if curr_node.left is not None:
            node_stack.append(curr_node.left)
        if curr_node.right is not None:
            node_stack.append(curr_node.right)

    return bfs   


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
#    ptsi = [(4.4, 1.9, 0), (4.2, -2.0, 1), (-2.3, -2.3, 2),
#           (-2.1, -2.5, 3), (-1.4, 2.5, 4), (4.6, -4.2, 5)]
    #       (-4.0, 4.3, 6)]
    ptsi = [(pts[i][0], pts[i][1], i+1) for i in range(len(pts))]
    kd2 = KDTree2D(ptsi)
    bfs = traverse_bfs(kd2.root) 
    with open('bfs.txt','w') as fh:
        for nd in bfs:
            fh.write(f'{nd.data[0]}, {nd.data[1]}, {nd.data[2]}\n')


