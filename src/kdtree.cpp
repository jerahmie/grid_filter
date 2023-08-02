#include <iostream>
#include <vector>
#include <tuple>
#include "kdtree_node.h"
#include "kdtree.h"

// Return the median data and index of a list
std::tuple<nodeData, int> median_point_id(const std::vector<nodeData> &nd) {
  int median_id = int(nd.size()/2);
  std::tuple<nodeData, int> median_node{nd.at(median_id), median_id};
  return std::tuple<nodeData, int>(median_node);
}


