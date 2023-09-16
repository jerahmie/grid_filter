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

// Projected distance (squared) between 2D points in given dimension.
double euclidean_1d_distance_sq(point2D p1, point2D p2, int dim) {
  double dist_sq = 0.0;
  if (dim == 0) {
    dist_sq = pow((p2.lat - p1.lat),2.0);  
  } else if (dim == 1) {
    dist_sq = pow((p2.lon - p1.lon),2.0);
  } else {
    dist_sq = -1.0; 
  }
  return dist_sq;
}

// Distance (squared) between 2D points.
double euclidean_2d_distance_sq(point2D p1, point2D p2) {
  return pow((p2.lat-p1.lat),2.0) + pow((p2.lon-p1.lon),2.0);
}
