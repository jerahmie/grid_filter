/*
 * File - kdtree.h
 */

#pragma once

#include <memory>
#include <tuple>
#include "kdtree_node.h"
#include "build_tree.h"

//std::tuple<nodeData, int> median_point_id(const std::vector<nodeData> &nd);

//KDTreeNode2D build_tree(std::vector<nodeData>&, int);

//KDTreeNode2D build_tree(std::vector<nodeData>&,
//                        std::vector<nodeData>::iterator,
//                        std::vector<nodeData>::iterator, int);

class KDTree {
  private:
    int depth;
    std::unique_ptr<nodeData> nd;
  public:
    KDTree(std::unique_ptr<nodeData> nd) : nd(std::move(nd)){}
    ~KDTree()=default;
    friend std::tuple<nodeData, int> median_point_id(const std::vector<nodeData>);
    friend KDTreeNode2D build_tree(std::vector<nodeData>&,
                                   std::vector<nodeData>::iterator,
                                   std::vector<nodeData>::iterator, int);
};
