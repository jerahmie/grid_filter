#include <iostream>
#include <vector>
#include "kdtree_node.h"
#include "kdtree.h"

int main(void) {
  std::cout << "<< Small 2D KD-tree example >>\n";

  std::vector<nodeData> node_vec{{0.12, 3.45, 2},
                                   {0.24, 6.8, 1},
                                   {0.35, 4.66, 0}};
  std::vector<nodeData>::iterator iter = node_vec.begin(); 
  std::cout << "<< Iterate over vector using iterator >>\n";
  for (iter; iter < node_vec.end(); iter++) {
    std::cout << *iter << '\n';
  }
  std::cout << "<< Iterate over vector using auto& >>\n";
  for (auto &elem : node_vec) {
    std::cout << elem << '\n';
  }

  KDTreeNode2D nlc {NULL, NULL, node_vec[0]};
  KDTreeNode2D nrc {NULL, NULL, node_vec[1]};
  KDTreeNode2D root {&nlc, &nrc, node_vec[2]};
  std::cout << root.getData().cell_index << '\n';
  std::cout << root.getLeft()->getData().cell_index << '\n';
  std::cout << root.getRight()->getData().cell_index << '\n';
}

