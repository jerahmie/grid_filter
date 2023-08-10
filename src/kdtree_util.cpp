/*
 * File - kdtree_util.cpp
 * KD Tree utility functions.
 */

#include <memory>
#include <cmath>
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

// Return the median data and index of a list
std::tuple<nodeData, int> median_point_id(const std::vector<nodeData> &nd) {
  int median_id = floor(nd.size()/2);
  std::tuple<nodeData, int> median_node{nd.at(median_id), median_id};
  return std::tuple<nodeData, int>(median_node);
}

