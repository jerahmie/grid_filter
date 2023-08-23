#pragma once

#include <vector>
#include "kdtree_node.h"

#define KD_DIM 2

KDTreeNode2D build_tree(std::vector<nodeData>&,
                        std::vector<nodeData>::iterator,
                        std::vector<nodeData>::iterator, int);

