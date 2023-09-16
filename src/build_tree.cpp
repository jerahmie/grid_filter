/*
 * file - build_tree.cpp
 * Helper function for constructing 2D KDTree form MPAS static data.
 */

#include <vector>
#include <memory>
#include <tuple>
#include <algorithm>
#include <cmath>
#include "kdtree_node.h"
#include "kdtree_util.h"
#include "build_tree.h"

// Recursively contruct a two dimensional KDTree from a vector of nodeData. 
KDTreeNode2D build_tree(std::vector<nodeData> &nd,
                        std::vector<nodeData>::iterator data_begin,
                        std::vector<nodeData>::iterator data_end, int depth) {

	std::size_t data_len = std::distance(data_begin, data_end);

  if (data_len == 1) {
		// Base case: KDTree leaf.
		// Returns a KDTree with root node with NULL left and right nodes.
    std::size_t index = std::distance(std::begin(nd), data_begin);
    return KDTreeNode2D(NULL, NULL, std::make_shared<nodeData>(nd[index]));
  } else {
		// Iterate to next KDTree dimension
    int dim = depth % KD_DIM;
		// Sort on latitude or longitude, depending on current depth
		std::sort(data_begin, data_end, (dim == 0)? compare_lat : compare_lon);
    depth++;

	  // Update iterators for start, mid and end locations in data vector.
    std::size_t data_mid = round(((double)data_len)/2.0);
    std::size_t mid_id = std::distance(std::begin(nd), data_begin + data_mid - 1);
    std::vector<nodeData>::iterator end_left, begin_right;
    end_left = data_begin + data_mid - 1;
    begin_right = data_begin + data_mid;
    KDTreeNode2D left_subtree, right_subtree ;
    std::shared_ptr<KDTreeNode2D> left_subtree_p = std::make_shared<KDTreeNode2D>(left_subtree);
    std::shared_ptr<KDTreeNode2D> right_subtree_p = std::make_shared<KDTreeNode2D>(right_subtree);

		// Recursively set left and right nodes to sub KD-trees.
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
