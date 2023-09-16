/*
 * file - build_tree.h
 * 
 * Helper function for constructing 2D KDtree from MPAS static data.
 */


#pragma once

#include <vector>
#include "kdtree_node.h"

#define KD_DIM 2

KDTreeNode2D build_tree(std::vector<nodeData>&,
                        std::vector<nodeData>::iterator,
                        std::vector<nodeData>::iterator, int);

