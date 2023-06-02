#include <iostream>
#include "kdtree_node.h"

std::ostream& operator<<(std::ostream& os, const nodeData& nd) {
  os << '(' << nd.lat << ", " << nd.lon << ", " << nd.cell_index << ')';
  return os;
}

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

std::ostream& operator<<(std::ostream& os, const KDTreeNode2D& kd2_node) {
  os << '(' << kd2_node.node_data << ')';
  return os;
}

nodeData KDTreeNode2D::getData(void) {
  // Return node data
  return node_data;
}
