#include <iostream>
#include "kdtree_node.h"

KDTreeNode2D::KDTreeNode2D(KDTreeNode2D* left_node, KDTreeNode2D* right_node, nodeData data) {
  left = left_node;
  right = right_node;
  data = data;
}

KDTreeNode2D* KDTreeNode2D::getLeft(void) {
  return left;
}

KDTreeNode2D* KDTreeNode2D::getRight(void) {
  return right;
}
