#include <iostream>
#include <vector>
#include <tuple>
#include "kdtree_node.h"
#include "kdtree_util.h"
#include "kdtree.h"


// Return the median data and index of a list
std::tuple<nodeData, int> median_point_id(const std::vector<nodeData> &nd) {
  int median_id = int(nd.size()/2);
  std::tuple<nodeData, int> median_node{nd.at(median_id), median_id};
  return std::tuple<nodeData, int>(median_node);
}

// Build a KDTree from nodeData vector
KDTreeNode2D build_tree(std::shared_ptr<std::vector<nodeData>> nd, int depth) {
  if (nd->size() == 1) {
    return KDTreeNode2D(NULL, NULL, std::make_shared<nodeData>((*nd)[0]));
  } else {

  nodeData ndr  {0.0, 0.0, 0};
  KDTreeNode2D tree_root = {NULL, NULL, std::make_shared<nodeData>(ndr)} ;

  return tree_root;
  }
};
