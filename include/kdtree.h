/*
 * File - kdtree.h
 */

#pragma once

#include <memory>
#include <tuple>
#include "kdtree_node.h"
#include "kdtree_util.h"
#include "build_tree.h"

class KDTree {
  private:
    int depth;
    int compares;
    std::vector<nodeData> nd;
    int nd_size;
  
  public:
    //KDTree(std::vector<nodeData> nd) : nd(std::move(nd)) {};
    double lat_min, lat_max, lon_min, lon_max;
    KDTreeNode2D root;
    std::shared_ptr<KDTreeNode2D> rootp;
    KDTree(std::vector<nodeData> nd);
    KDTree(std::string);
    KDTree(std::string, std::vector<int>);
    ~KDTree()=default;
    int size(void) {return nd_size;}
    std::tuple<double, int, int> nearest_cell_recursive(point2D&, std::shared_ptr<KDTreeNode2D>, int);
    int find_nearest_cell_type(double, double); 
    int find_nearest_cell_id(double, double); 
    friend std::tuple<nodeData, int> median_point_id(const std::vector<nodeData>);
    friend KDTreeNode2D build_tree(std::vector<nodeData>&,
                                   std::vector<nodeData>::iterator,
                                   std::vector<nodeData>::iterator, int);
};
