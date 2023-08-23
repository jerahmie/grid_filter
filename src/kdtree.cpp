#include <iostream>
#include <vector>
#include <tuple>
#include <algorithm>
#include <cmath>
#include <string>
#include "mpas_file.h"
#include "mpas_util.h"
#include "kdtree_node.h"
#include "kdtree_util.h"
#include "kdtree.h"

// radians to degrees conversion factor
constexpr float rad_to_deg(float &r) {
  return (float)(r*180.0/(atan(1.0)*4.0));
}

//KDTree::KDTree(std::vector<nodeData> nd) : nd(std::move(nd)) {
// Construct KDTree from vector of node data.
KDTree::KDTree(std::vector<nodeData> nd) : nd (nd) {
  nd_size = nd.size();
  root = build_tree(nd, nd.begin(), nd.end(), 0);
  rootp = std::make_shared<KDTreeNode2D>(root);
}

// Construct KDTree from MPAS Static File.
KDTree::KDTree(std::string filename){
  MPASFile mpf = MPASFile(filename);
  int ncells = mpf.read_dim("nCells");
  std::vector<float> lats = mpf.read_var_1d_float("latCell", ncells);
  for (auto i = lats.begin(); i < lats.end(); i++ ) {*i = rad_to_deg(*i);}
  std::vector<float> lons = mpf.read_var_1d_float("lonCell", ncells);
  for (auto i = lons.begin(); i < lons.end(); i++ ) {*i = rad_to_deg(*i);}
  nd = merge_lat_lon(lats, lons);
  nd_size = nd.size();
  root = build_tree(nd, nd.begin(), nd.end(), 0);
  rootp = std::make_shared<KDTreeNode2D>(root);
}

// Construct KDTree from MPAS Static File and filter by boundary cell type.
KDTree::KDTree(std::string filename, std::vector<int> bdy_cell_type){
  // Read cells
  MPASFile mpf = MPASFile(filename);
  int ncells = mpf.read_dim("nCells");
  std::vector<float> lats = mpf.read_var_1d_float("latCell", ncells);
  for (auto i = lats.begin(); i < lats.end(); i++ ) {*i = rad_to_deg(*i);}
  std::vector<float> lons = mpf.read_var_1d_float("lonCell", ncells);
  for (auto i = lons.begin(); i < lons.end(); i++ ) {*i = rad_to_deg(*i);}
  std::vector<int> bdy_cells = mpf.read_var_1d_int("bdyMaskCell", ncells);
  // create and filter nodes by cell type
  std::vector<nodeData> nd_unfiltered = merge_lat_lon(lats, lons, bdy_cells);
  nd = filter_bdy_mask_cell(nd_unfiltered, bdy_cells, bdy_cell_type); 
  nd_size = nd.size(); 
  root = build_tree(nd, nd.begin(), nd.end(), 0);
  rootp = std::make_shared<KDTreeNode2D>(root);
}

// Find the nearest cell index given a pair of lat/lon values.
std::tuple<double, int, int> KDTree::nearest_cell_recursive(point2D &qpt,
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
    return std::tuple<double, int, int>(w_node, node->getData()->cell_index, node->getData()->bdy_cell_type);
  } else if ( (node->getLeft() != NULL ) and (node->getRight() == NULL) ) {
    // Node with right child only.
    double w = 0.0;
    int nearest_cell;
    int nearest_bdy_cell; 
    std::tuple<double, int, int> nearest_cell_left = nearest_cell_recursive(qpt, node->getLeft(), depth);
    double w_left = std::get<0>(nearest_cell_left);
    int nearest_cell_left_id = std::get<1>(nearest_cell_left);
    int nearest_bdy_cell_left = std::get<2>(nearest_cell_left);
    if (w_left < w_node){
      w = w_left;
      nearest_cell = nearest_cell_left_id;
      nearest_bdy_cell = nearest_bdy_cell_left;
    } else {
      w = w_node;
      nearest_cell = node->getData()->cell_index;
      nearest_bdy_cell = node->getData()->bdy_cell_type;
    }
    return std::tuple<double, int, int>(w, nearest_cell, nearest_bdy_cell);
  } else if ( (node->getLeft() == NULL ) and (node->getRight() != NULL) ) {
    // Node with left child only.
    double w = 0.0;
    int nearest_cell;
    int nearest_bdy_cell;
    std::tuple<double, int, int> nearest_cell_right = nearest_cell_recursive(qpt, node->getRight(), depth);
    double w_right = std::get<0>(nearest_cell_right);
    int nearest_cell_right_id = std::get<1>(nearest_cell_right);
    int nearest_bdy_cell_right = std::get<2>(nearest_cell_right);
    if (w_right < w_node){
      w = w_right;
      nearest_cell = nearest_cell_right_id;
      nearest_bdy_cell = nearest_bdy_cell_right;
    } else {
      w = w_node;
      nearest_cell = node->getData()->cell_index;
    }
    return std::tuple<double, int, int>(w, nearest_cell, nearest_bdy_cell);
  } else {
    // Node with right and left child.
    //
    // consider points near cutoff
    double w = 0.0;
    double qpt_dim, nd_dim;
    int nearest_cell, nearest_bdy_cell;
    if (dim == 0) {
      qpt_dim = qpt.lat;
      nd_dim = node->getData()->lat;
    } else {
      qpt_dim = qpt.lon;
      nd_dim = node->getData()->lon;
    }
    if (qpt_dim < nd_dim) {
      std::tuple<double, int, int> nearest_cell_left = nearest_cell_recursive(qpt, node->getLeft(), depth);
      double w_left = std::get<0>(nearest_cell_left);
      int nearest_cell_id_left = std::get<1>(nearest_cell_left);
      int nearest_bdy_cell_left = std::get<2>(nearest_cell_left);
      if (w_left < w_node) {
        w = w_left;
        nearest_cell = nearest_cell_id_left;
        nearest_bdy_cell = nearest_bdy_cell_left;
      } else {
        w = w_node;
        nearest_cell = node->getData()->cell_index;
        nearest_bdy_cell = node->getData()->bdy_cell_type;
      }
      point2D node_pt = point2D {node->getData()->lat, node->getData()->lon};
      if ((euclidean_1d_distance_sq(qpt, node_pt, dim) < w) and 
          (node->getRight() != NULL)) {
        std::tuple<double, int, int> nearest_cell_alt = nearest_cell_recursive(qpt, node->getRight(), depth);
        double w_test_alt = std::get<0>(nearest_cell_alt);
        int nearest_cell_id_alt = std::get<1>(nearest_cell_alt);
        int nearest_bdy_cell_alt = std::get<2>(nearest_cell_alt);
        if (w_test_alt < w) {
          w = w_test_alt;
          nearest_cell = nearest_cell_id_alt;
          nearest_bdy_cell = nearest_bdy_cell_alt;
        }
      }
    } else {
      std::tuple<double, int, int> nearest_cell_right = nearest_cell_recursive(qpt, node->getRight(), depth);
      double w_right = std::get<0>(nearest_cell_right);
      int nearest_cell_id_right = std::get<1>(nearest_cell_right);
      int nearest_bdy_cell_right = std::get<2>(nearest_cell_right);

      if (w_right < w_node) {
        w = w_right;
        nearest_cell = nearest_cell_id_right;
        nearest_bdy_cell = nearest_bdy_cell_right;
      } else {
        w = w_node;
        nearest_cell = node->getData()->cell_index;
        nearest_bdy_cell = node->getData()->bdy_cell_type;
      }
      point2D node_pt = point2D {node->getData()->lat, node->getData()->lon};
      if ((euclidean_1d_distance_sq(qpt, node_pt, dim) < w) and 
          (node->getLeft() != NULL)) {
        std::tuple<double, int, int> nearest_cell_alt = nearest_cell_recursive(qpt, node->getLeft(), depth);
        double w_test_alt = std::get<0>(nearest_cell_alt);
        int nearest_cell_id_alt = std::get<1>(nearest_cell_alt);
        int nearest_bdy_cell_alt = std::get<2>(nearest_cell_alt);
        if (w_test_alt < w) {
          w = w_test_alt;
          nearest_cell = nearest_cell_id_alt;
          nearest_bdy_cell = nearest_bdy_cell_alt;
        }
      }
    }
    return std::tuple<double, int, int>(w, nearest_cell, nearest_bdy_cell);
  }
}

int KDTree::find_nearest_cell_id(double lat, double lon){
  // return the nearest cell in our kdtree.
  point2D q {lat, lon};
  std::tuple<double, int, int> nearest = nearest_cell_recursive(q, rootp, 0);
  int nearest_cell_id = std::get<1>(nearest);
  return nearest_cell_id; 
}

int KDTree::find_nearest_cell_type(double lat, double lon){
  // return the nearest cell in our kdtree.
  point2D q {lat, lon};
  std::tuple<double, int, int> nearest = nearest_cell_recursive(q, rootp, 0);
  int nearest_cell_type = std::get<2>(nearest);
  return nearest_cell_type; 
}
