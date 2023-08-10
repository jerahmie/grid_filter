#include <iostream>
#include <vector>
#include <tuple>
#include <algorithm>
#include "kdtree_node.h"
#include "kdtree_util.h"
#include "kdtree.h"

//class KDTree {
//  private:
//    int depth;
//    std::unique_ptr<nodeData> nd;
//  public:
//    KDTree(std::unique_ptr<nodeData> nd) : nd(std::move(nd)){}
//    ~KDTree()=default;
//    friend std::tuple<nodeData, int> median_point_id(const std::vector<nodeData>);
//    friend KDTreeNode2D build_tree(std::vector<nodeData>&,
//                                   std::vector<nodeData>::iterator,
//                                   std::vector<nodeData>::iterator, int);
//};

//KDTree::KDTree(std::unique_ptr<nodeData>nd) : nd(std::move(nd)) {

//}

