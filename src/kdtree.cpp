#include <iostream>
#include <vector>
#include <tuple>
#include <algorithm>
#include "kdtree_node.h"
#include "kdtree_util.h"
#include "kdtree.h"

#define KD_DIM 2

// Return the median data and index of a list
std::tuple<nodeData, int> median_point_id(const std::vector<nodeData> &nd) {
  int median_id = int(nd.size()/2);
  std::tuple<nodeData, int> median_node{nd.at(median_id), median_id};
  return std::tuple<nodeData, int>(median_node);
}

// Build a KDTree from nodeData vector
KDTreeNode2D build_tree(std::vector<nodeData> &nd,
                        std::vector<nodeData>::iterator data_begin,
                        std::vector<nodeData>::iterator data_end, int depth) {


  if (std::distance(data_begin, data_end) == 1) {
    std::size_t index = std::distance(std::begin(nd), data_begin);
    return KDTreeNode2D(NULL, NULL, std::make_shared<nodeData>(nd[index]));
  } else {
    int dim = depth % KD_DIM; 
    
    std::sort(data_begin, data_end, (dim == 0)? compare_lat : compare_lon);

    std::size_t data_len = std::distance(data_begin, data_end); 
    std::size_t data_mid = data_len/2;

    std::size_t mid_id = std::distance(std::begin(nd), data_begin + data_mid);
    std::vector<nodeData>::iterator end_left, begin_right;
    end_left = data_begin + data_mid;
    begin_right = data_begin + data_mid + 1;

    depth++;
    KDTreeNode2D left_subtree, right_subtree ;
    std::shared_ptr<KDTreeNode2D> left_subtree_p = std::make_shared<KDTreeNode2D>(left_subtree);
    std::shared_ptr<KDTreeNode2D> right_subtree_p = std::make_shared<KDTreeNode2D>(right_subtree);
    
    if (std::distance(begin_right, data_end) > 0) {
      *right_subtree_p = build_tree(nd, begin_right, data_end, depth);
    } else {
      right_subtree_p.reset();
    }
    if (std::distance(data_begin, end_left) > 0) {
      *left_subtree_p = build_tree(nd, data_begin, end_left, depth);
    } else {
      left_subtree_p.reset();
    }
 
    return KDTreeNode2D(left_subtree_p, right_subtree_p,
                        std::make_shared<nodeData>(nd[mid_id]));
  }
};
