/*
 * mpas_util.cpp
 * Utility and helper functions for generating kd-trees from MPAS 
 * Regional static data.
 */
#include <iostream>
#include <vector>
#include <algorithm>
#include <tuple>
#include <stdexcept>
#include <limits>
#include "kdtree_node.h"
#include "mpas_util.h"


// Merge latitude and longitude data into vector of node data.
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

// Merge latitude and longitude data into vector of node data.
std::vector<nodeData> merge_lat_lon(std::vector<float>& lat,
                                    std::vector<float>& lon, 
                                    std::vector<int>& bdy_cell) {
  std::vector<nodeData> nd;
  if ( lat.size() != lon.size() ) {
    throw std::invalid_argument("Input vectors must be same length.");
  } 

  int ncells = lat.size(); 
  for (int i = 0; i < ncells; i++) {
    nd.push_back({lat[i], lon[i], i+1, bdy_cell[i]});
  }
  return nd;
}


// Filter nodes by boundary cell type.
std::vector<nodeData> filter_bdy_mask_cell(std::vector<nodeData> &nodes,
                                           std::vector<int> &bdy_cells,
                                           std::vector<int> &bdy_cell_type) {
  std::vector<nodeData> filtered_cells;
  std::vector<int>::iterator it;
  int bdy_match_index = 0;
  for (it=bdy_cells.begin(); it<bdy_cells.end(); it++){
    if (std::find(bdy_cell_type.begin(), bdy_cell_type.end(), *it) != bdy_cell_type.end())
    {
      bdy_match_index = it-bdy_cells.begin();
      filtered_cells.push_back(nodes[bdy_match_index]);
    }
  }
  return filtered_cells;
}

// Find the min/max latitude and longitudes
MPASMinMax find_min_max(std::vector<nodeData> &data_points) {
  MPASMinMax minmax {std::numeric_limits<double>::max(), 
                    -1.0*std::numeric_limits<double>::max(),
                    std::numeric_limits<double>::max(),
                    -1.0*std::numeric_limits<double>::max()}; 
  for (auto node : data_points) {
    if (node.lat < minmax.LatMin) { minmax.LatMin = node.lat;}
    if (node.lat > minmax.LatMax) { minmax.LatMax = node.lat;}
    if (node.lon < minmax.LonMin) { minmax.LonMin = node.lon;}
    if (node.lon > minmax.LonMax) { minmax.LonMax = node.lon;}
  }

  return minmax;
}
