/*
 * kdtree_bfs.cpp
 * Dump a kdtree with a breadth-first search.
 *
 */
#include <iostream>
#include <fstream>
#include <cassert>
#include <vector>
#include <queue>
#include "mpas_file.h"
#include "kdtree_node.h"
#include "kdtree.h"

std::vector<nodeData> traverse_bfs(const KDTreeNode2D & kd2d) {
  std::vector<nodeData> bfs;
  std::queue<nodeData> ndq;
  for (auto i : bfs) {
    std::cout << i << '\n';
  }
  return bfs;
}

int main(int argc, char* argv[]) {
  std::cout << "KD-Tree Traversal, Breadth First.\n";
  std::cout << "argc: " << argc << '\n';
  assert(argc == 2); 

}
