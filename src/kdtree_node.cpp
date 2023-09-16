/*
 * file - kdtree_node.cpp
 * KDTree consists of KDTreeNode2D nodes that consists of data (lat, lon, id)
 * and pointers to left and right nodes.
 *
 */

#include <iostream>
#include <memory>
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

KDTreeNode2D::KDTreeNode2D(std::shared_ptr<KDTreeNode2D> nl, 
    std::shared_ptr<KDTreeNode2D> nr, 
    std::shared_ptr<nodeData> nd) :  node_left{nl}, node_right{nr}, node_data{nd} {}

std::shared_ptr<KDTreeNode2D> KDTreeNode2D::getLeft(void) {
  // Return pointer to the left child node
  return node_left;
}

std::shared_ptr<KDTreeNode2D> KDTreeNode2D::getRight(void) {
  // Return pointer to the right child node
  return node_right;
}

std::ostream& operator<<(std::ostream& os, const KDTreeNode2D& kd2_node) {
  os << '(' << kd2_node.node_data << ')';
  return os;
}

std::shared_ptr<nodeData> KDTreeNode2D::getData(void) {
  // Return node data
  return node_data;
}
