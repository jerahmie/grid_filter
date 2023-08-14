/*
 * File - kdtree_util.cpp
 * KD Tree utility functions.
 */
#include <iostream>
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

float euclidean_1d_distance_sq(nodeData n1, nodeData n2, int dim) {
  float dist_sq = 0.0;
  if (dim == 0) {
    dist_sq = pow((n2.lat - n1.lat),2.0);  
  } else if (dim == 1) {
    dist_sq = pow((n2.lon - n1.lon),2.0);
  } else {
    dist_sq = -1.0; 
  }
  return dist_sq;
}

float euclidean_2d_distance_sq(nodeData n1, nodeData n2) {
  return pow((n2.lat-n1.lat),2.0) + pow((n2.lon-n1.lon),2.0);
}
