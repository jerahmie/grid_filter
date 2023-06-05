#include <iostream>
#include "kdtree_node.h"


// compare node data along dimension
bool compare_node_lat(nodeData n1, nodeData n2) {
  return (n1.lat < n2.lat);
}

// compare node data along dimension
bool compare_node_lon(nodeData n1, nodeData n2) {
  return (n1.lon < n2.lon);
}

// Overload operator== to compare if two nodeData are equal
bool operator==(const nodeData& lhs, const nodeData& rhs) {
  return (lhs.lat == rhs.lat) &&
         (lhs.lon == rhs.lon) &&
         (lhs.cell_index == rhs.cell_index);
}
bool operator!=(const nodeData& lhs, const nodeData& rhs) {
  return (lhs.lat != rhs.lat) ||
         (lhs.lon != rhs.lon) ||
         (lhs.cell_index != rhs.cell_index);
}

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
