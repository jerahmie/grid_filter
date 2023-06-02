#include <iostream>
#include <vector>
#include <algorithm>
#include "kdtree_node.h"

int main(void) {
  std::cout << "<< Small 2D KD-tree example >>\n";
  std::vector<double> dvec{3.59, 3.99, 4.88, 0.87, 3.33,
                           0.21, 1.35, 0.54, 3.14, 0.48};
 
  std::sort(dvec.begin(), dvec.end());

  for (auto &elem : dvec) {
    std::cout << elem << ' ';
  }
  std::cout << '\n';

  std::vector<nodeData> node_vec{{0.56, 1.71, 0},
                                 {0.45, 0.32, 1},
                                 {0.73, 0.19, 2},
                                 {0.09, 1.65, 3},
                                 {0.67, 0.03, 4},
                                 {0.32, 0.87, 5},
                                 {0.56, 1.26, 6},
                                 {0.0, 1.6, 7},
                                 {0.17, 1.82, 8},
                                 {0.56, 1.07, 9},
                                 {0.37, 0.11, 10},
                                 {0.3, 0.86, 11},
                                 {0.05, 1.59, 12},
                                 {0.47, 1.56, 13},
                                 {0.91, 0.18, 14},
                                 {0.06, 1.35, 15},
                                 {0.84, 0.43, 16},
                                 {0.36, 0.46, 17},
                                 {0.5, 1.05, 18},
                                 {0.59, 1.77, 19}};

  std::vector<nodeData>::iterator iter = node_vec.begin(); 
  std::cout << "<< Iterate over vector using iterator >>\n";
  for (iter; iter < node_vec.end(); iter++) {
    std::cout << (*iter).lat << '\n';
  }
  std::cout << "<< Iterate over vector using auto& >>\n";
  for (auto &elem : node_vec) {
    std::cout << elem << '\n';
  }

  std::cout << "<< Sort 2D points by latitude." << '\n';
  std::sort(node_vec.begin(), node_vec.end(), compare_node_lat);
  for (auto &elem : node_vec) {
    std::cout << elem.lat << ' ';
  }
  std::cout << '\n';

  std::cout << "<< Sort 2D points by longitude." << '\n';
  std::sort(node_vec.begin(), node_vec.end(), compare_node_lon);
  for (auto &elem : node_vec) {
    std::cout << elem.lon << ' ';
  }
  std::cout << '\n'; 
  KDTreeNode2D nlc {NULL, NULL, node_vec[0]};
  KDTreeNode2D nrc {NULL, NULL, node_vec[1]};
  KDTreeNode2D root {&nlc, &nrc, node_vec[2]};
  std::cout << root.getData().cell_index << '\n';
  std::cout << root.getLeft()->getData().cell_index << '\n';
  std::cout << root.getRight()->getData().cell_index << '\n';
}

