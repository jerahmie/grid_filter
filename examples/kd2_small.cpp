#include <iostream>
#include <vector>
#include "kdtree_node.h"
#include "kdtree.h"

int main(void) {
  std::vector<nodeData> node_data {{0.12, 3.45, 0},
                                   {0.24, 6.8, 1},
                                   {0.35, 4.66, 2}};
  
  std::cout << "<< Small 2D KD-tree example >>\n";
  KDTreeNode2D nlc {NULL, NULL, node_data[0]};
  KDTreeNode2D nrc {NULL, NULL, node_data[1]};
  KDTreeNode2D root {&nlc, &nrc, node_data[2]};
  std::cout << root.getData().cell_index << '\n';
  std::cout << root.getLeft()->getData().cell_index << '\n';
  std::cout << root.getRight()->getData().cell_index << '\n';
}

