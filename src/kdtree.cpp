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
  rootp = std::make_shared<KDTreeNode2D>(root);
}

// Find the nearest cell index given a pair of lat/lon values.
std::tuple<double, int> KDTree::nearest_cell_recursive(point2D &qpt,
                                                      std::shared_ptr<KDTreeNode2D> node,
                                                      int depth) {
  point2D node_pt {node->getData()->lat, node->getData()->lon};
  // update number of compares counter for KD-Tree search.
  compares++;
  // update state variable 
  int dim = depth%2;
  depth++;
  
  //visited_points.push_back(node.cell_index);
  double w_node = euclidean_2d_distance_sq(qpt, node_pt);
  if ( ( node->getLeft() == NULL ) and (node->getRight() == NULL ) ) {
    // Leaf node
    return std::tuple<double, int>(w_node, node->getData()->cell_index);
  } else if ( (node->getLeft() != NULL ) and (node->getRight() == NULL) ) {
    // Node with right child only.
    double w = 0.0;
    int nearest_cell;
    std::tuple<double, int> nearest_cell_left = nearest_cell_recursive(qpt, node->getLeft(), depth);
    double w_left = std::get<0>(nearest_cell_left);
    int nearest_cell_left_id = std::get<1>(nearest_cell_left);
    if (w_left < w_node){
      w = w_left;
      nearest_cell = nearest_cell_left_id;
    } else {
      w = w_node;
      nearest_cell = node->getData()->cell_index;
    }
    return std::tuple<double, int>(w, nearest_cell);
  } else if ( (node->getLeft() == NULL ) and (node->getRight() != NULL) ) {
    // Node with left child only.
    double w = 0.0;
    int nearest_cell;
    std::tuple<double, int> nearest_cell_right = nearest_cell_recursive(qpt, node->getRight(), depth);
    double w_right = std::get<0>(nearest_cell_right);
    int nearest_cell_right_id = std::get<1>(nearest_cell_right);
    if (w_right < w_node){
      w = w_right;
      nearest_cell = nearest_cell_right_id;
    } else {
      w = w_node;
      nearest_cell = node->getData()->cell_index;
    }
    return std::tuple<double, int>(w, nearest_cell);
  } else {
    // Node with right and left child.
    //
    // consider points near cutoff
    double w = 0.0;
    double qpt_dim, nd_dim;
    int nearest_cell;
    if (dim == 0) {
      qpt_dim = qpt.lat;
      nd_dim = node->getData()->lat;
    } else {
      qpt_dim = qpt.lon;
      nd_dim = node->getData()->lon;
    }
    if (qpt_dim < nd_dim) {
      std::tuple<double, int> nearest_cell_left = nearest_cell_recursive(qpt, node->getLeft(), depth);
      double w_left = std::get<0>(nearest_cell_left);
      int nearest_cell_id_left = std::get<1>(nearest_cell_left);
      if (w_left < w_node) {
        w = w_left;
        nearest_cell = nearest_cell_id_left;
      } else {
        w = w_node;
        nearest_cell = node->getData()->cell_index;
      }
      point2D node_pt = point2D {node->getData()->lat, node->getData()->lon};
      if ((euclidean_1d_distance_sq(qpt, node_pt, dim) < w) and 
          (node->getRight() != NULL)) {
        std::tuple<double, int> nearest_cell_alt = nearest_cell_recursive(qpt, node->getRight(), depth);
        double w_test_alt = std::get<0>(nearest_cell_alt);
        int nearest_cell_id_alt = std::get<1>(nearest_cell_alt);
        if (w_test_alt < w) {
          w = w_test_alt;
          nearest_cell = nearest_cell_id_alt;
        }
      }
    } else {
      std::tuple<double, int> nearest_cell_right = nearest_cell_recursive(qpt, node->getRight(), depth);
      double w_right = std::get<0>(nearest_cell_right);
      int nearest_cell_id_right = std::get<1>(nearest_cell_right);
      if (w_right < w_node) {
        w = w_right;
        nearest_cell = nearest_cell_id_right;
      } else {
        w = w_node;
        nearest_cell = node->getData()->cell_index;
      }
      point2D node_pt = point2D {node->getData()->lat, node->getData()->lon};
      if ((euclidean_1d_distance_sq(qpt, node_pt, dim) < w) and 
          (node->getLeft() != NULL)) {
        std::tuple<double, int> nearest_cell_alt = nearest_cell_recursive(qpt, node->getLeft(), depth);
        double w_test_alt = std::get<0>(nearest_cell_alt);
        int nearest_cell_id_alt = std::get<1>(nearest_cell_alt);
        if (w_test_alt < w) {
          w = w_test_alt;
          nearest_cell = nearest_cell_id_alt;
        }
      }
    }
    return std::tuple<double, int>(w, nearest_cell);
  }
}

int KDTree::find_nearest_cell_id(double lat, double lon){
  // return the nearest cell in our kdtree.
  point2D q {lat, lon};
  std::tuple<double, int> nearest = nearest_cell_recursive(q, rootp, 0);

  int nearest_cell_id = std::get<1>(nearest);
  return nearest_cell_id; 
}
