#include <iostream>
#include "kdtree_node.h"

KDTreeNode2D::KDTreeNode2D(KDTreeNode2D* left_node, KDTreeNode2D* right_node, nodeData nd) {
  left = left_node;
  right = right_node;
  node_data = nd;
}

KDTreeNode2D* KDTreeNode2D::getLeft(void) {
  // Return pointer to the left child node
  return left;
}

KDTreeNode2D* KDTreeNode2D::getRight(void) {
  // Return pointer to the right child node
  return right;
}

nodeData KDTreeNode2D::getData(void) {
  // Return node data
  return node_data;
}
