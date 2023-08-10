/*
 * mpas_util.cpp
 * Utility and helper functions for generating kd-trees from MPAS 
 * Regional static data.
 */
#include <iostream>
#include <vector>
#include <stdexcept>
#include "kdtree_node.h"
#include "mpas_util.h"

std::vector<nodeData> merge_lat_lon(std::vector<float>& lat,
                                    std::vector<float>& lon) {
  std::vector<nodeData> nd;
  if ( lat.size() != lon.size() ) {
    throw std::invalid_argument("Input vectors must be same length.");
  } 

  int ncells = lat.size(); 
  for (int i = 0; i < ncells; i++) {
    nd.push_back({lat[i], lon[i], i+1});
  }
  return nd;
}
