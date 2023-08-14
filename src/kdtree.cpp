#include <iostream>
#include <vector>
#include <tuple>
#include <algorithm>
#include "kdtree_node.h"
#include "kdtree_util.h"
#include "kdtree.h"

//KDTree::KDTree(std::vector<nodeData> nd) : nd(std::move(nd)) {
KDTree::KDTree(std::vector<nodeData> nd) : nd (nd) {
  root = build_tree(nd, nd.begin(), nd.end(), 0);
}

// Find the nearest cell index given a pair of lat/lon values.
int KDTree::nearest_cell(float lat, float lon){
  return 0; 
}
