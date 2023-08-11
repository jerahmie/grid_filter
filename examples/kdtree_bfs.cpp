/*
 * kdtree_bfs.cpp
 * Dump a kdtree with a breadth-first search.
 *
 */
#include <iostream>
#include <iomanip>
#include <fstream>
#include <cassert>
#include <vector>
#include <queue>
#include <cmath>
#include "mpas_file.h"
#include "mpas_util.h"
#include "kdtree_node.h"
#include "build_tree.h"
#include "kdtree.h"

// precompute conversion of radian to degree factor (180/pi).
constexpr float rad_to_deg (float& r) {
  return (float)(r*180.0/(atan(1.0)*4.0));
}


std::vector<nodeData> traverse_bfs( const KDTreeNode2D & kd2d) {
  std::vector<nodeData> bfs;
  std::queue<KDTreeNode2D> ndq;
  ndq.push(kd2d);
  while (!ndq.empty()) {
    if (ndq.front().getLeft() != NULL) {
      ndq.push(*(ndq.front().getLeft()));
    }
    if (ndq.front().getRight() != NULL) {
      ndq.push(*(ndq.front().getRight()));
    }
    bfs.push_back(*(ndq.front().getData()));
    ndq.pop();
  } 
  return bfs;
}

int main(int argc, char* argv[]) {

  std::cout << "KD-Tree Traversal, Breadth First.\n";
  if (argc != 2) {
    throw std::invalid_argument("Usage: kdtree_bsf 'Filename'.");
  }
  std::string mpas_loc = std::string(argv[1]);
  MPASFile mpf = MPASFile(mpas_loc);
  int ncells = mpf.read_dim("nCells");
  std::cout << "nCells: " << ncells << '\n';
  std::vector<float> lat = mpf.read_var_1d_float("latCell", ncells);
  std::vector<float> lon = mpf.read_var_1d_float("lonCell", ncells);
  std::vector<nodeData> lat_lon = merge_lat_lon(lat, lon);
  const KDTreeNode2D kd2d_root = build_tree(lat_lon, lat_lon.begin(), lat_lon.end(), 0);
 
  std::vector<nodeData> bfs = traverse_bfs(kd2d_root);
  std::ofstream of;
  of.open("bfs_cpp.txt");
  for (auto &nd : bfs) {
    of << std::fixed << std::setprecision(6) << nd.lat << ", " <<  nd.lon << ", " << nd.cell_index << '\n';
  }
  of.close();
  std::cout << "length bfs: " << bfs.size() << '\n';
}
