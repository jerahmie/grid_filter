/*
 * File - kdtree.h
 */

#pragma once

#include <memory>
#include <tuple>
#include "kdtree_node.h"
#include "build_tree.h"

class KDTree {
  private:
    int depth;
    std::vector<nodeData> nd;
    KDTreeNode2D root;
  public:
    //KDTree(std::vector<nodeData> nd) : nd(std::move(nd)) {};
    KDTree(std::vector<nodeData> nd);
    ~KDTree()=default;
    int nearest_cell(float, float);
    friend std::tuple<nodeData, int> median_point_id(const std::vector<nodeData>);
    friend KDTreeNode2D build_tree(std::vector<nodeData>&,
                                   std::vector<nodeData>::iterator,
                                   std::vector<nodeData>::iterator, int);
};
