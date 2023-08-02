/*
 * File - kdtree.h
 */

#pragma once

#include <memory>
#include "kdtree_node.h"
#include "tuple"

std::tuple<nodeData, int> median_point_id(const std::vector<nodeData> &nd);

class KDTree {
  private:
    int depth;
    std::unique_ptr<nodeData> nd;
  public:
    KDTree(std::unique_ptr<nodeData> nd) : nd(std::move(nd)){}

    ~KDTree()=delete;
    friend std::tuple<nodeData, int> median_point_id(const std::vector<nodeData>);
};
