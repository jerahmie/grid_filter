/*
 * File - kdtree_util.cpp
 * KD Tree utility functions.
 */

#include <memory>
#include "kdtree_node.h"
#include "kdtree_util.h"

// Compare latitude component of nodeData
bool compare_lat(nodeData d1, nodeData d2) {
  return (d1.lat < d2.lat);
}

// Compare longitude component of nodeData
bool compare_lon(nodeData d1, nodeData d2) {
  return (d1.lon < d2.lon);
}
