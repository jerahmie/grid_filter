#include <iostream>
#include <vector>
#include <tuple>
#include "kdtree_node.h"
#include "kdtree.h"

//std::tuple<nodeData, int> median_point_id(const std::vector<nodeData> &nd) {
std::tuple<nodeData, int> median_point_id(const std::vector<nodeData> &nd) {
  int median_id = int(nd.size()/2);
  std::tuple<nodeData, int> median_node{nd.at(median_id), median_id};
  return median_node;
}


