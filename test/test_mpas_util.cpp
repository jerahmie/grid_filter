/*
 * File - test_mpas_util.cpp
 */

#include <iostream>
#include <vector>
#include <string>
#include <tuple>
#include <stdexcept>
#include <catch2/catch_test_macros.hpp>
#include "mpas_util.h"
#include "kdtree_node.h"

std::vector<float> lats{ 0.77, 0.51, 0.82, 0.89, 0.53,
                         0.34, 0.67, 0.99, 0.92, 0.15 };

std::vector<float> lons{ 0.69, 0.31, 0.90, 0.75, 0.02,
                         0.18, 0.17, 0.09, 0.90, 0.39 };
float eps = 0.0001; // a small number for comparison

TEST_CASE("Test catch2 setup.", "[test_mpas_util]") {
  REQUIRE(42 == 42);
}

TEST_CASE("Test merge_lat_lon throw", "[test_mpas_util]") {
  // Verify that merge_lat_lon will throw exception if arguments have
  // differing shapes.
  std::vector<float> lats3 { 0.1, 2.3, 3.4 };
  std::vector<float> lons2 { 6.1, 5.3 };
  std::vector<float> lons3 { 0.1, 2.3, 3.4 };
  REQUIRE_THROWS_AS(merge_lat_lon(lats3, lons2), std::invalid_argument);
  REQUIRE_NOTHROW(merge_lat_lon(lats3, lons3));
}

TEST_CASE("Test merge_lat_lon values.", "[test_mpas_util]") {
 std::vector<nodeData> nd;
 nd = merge_lat_lon(lats, lons);
 std::cout << "nodes: \n";
 REQUIRE(nd.size() == 10);
 for (int i=0; i<(int)nd.size(); i++) {
   std::cout << nd[i].lat << ", " << nd[i].lon << ", " << nd[i].cell_index << '\n'; 
   REQUIRE(nd[i].lat == lats[i]);
   REQUIRE(nd[i].lon == lons[i]);
   REQUIRE(nd[i].cell_index == i+1);
 }
}

TEST_CASE("Test filter_bdy_mask_cell.", "[test_mpas_util]") {
  std::vector<nodeData> nd = merge_lat_lon(lats, lons);
  std::vector<int> bdy_cells = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
  std::vector<int> bdy_cell_type = {6, 7};
  std::vector<nodeData> nd_filtered = filter_bdy_mask_cell( nd, bdy_cells, bdy_cell_type);
  for (auto &nf : nd_filtered) {
    std::cout << "Filtered nodes: " << nf << '\n';
  }
  REQUIRE(nd_filtered.size() == 2);
  REQUIRE(nd_filtered[0].cell_index == 7);
  REQUIRE(nd_filtered[1].cell_index == 8);
}

TEST_CASE("Test find max min lat lon.", "[test_mpas_util]") {
  std::vector<nodeData> nd = merge_lat_lon(lats, lons);
  MPASMinMax minmax = find_min_max(nd);
  REQUIRE( (minmax.LatMin - 0.15) < eps );
  REQUIRE( (minmax.LatMax - 0.99) < eps );
  REQUIRE( (minmax.LonMin - 0.02) < eps );
  REQUIRE( (minmax.LonMax - 0.90) < eps );
}

TEST_CASE("Test alt max min lat lon.", "[test_mpas_util]") {
  std::vector<float> alt_lats {720.0, -120.0, 530.0, 10.0, -1.0};
  std::vector<float> alt_lons {-360.0, 200.0, 1001.1, 5150.0, 4.2};
  std::vector<nodeData> nd = merge_lat_lon(alt_lats, alt_lons);
  MPASMinMax minmax = find_min_max(nd);
  REQUIRE( abs(minmax.LatMin - (-120.0)) < eps );
  REQUIRE( abs(minmax.LatMax - (720.0)) < eps );
  REQUIRE( abs(minmax.LonMin - (-360.0)) < eps );
  REQUIRE( abs(minmax.LonMax - (5150.0)) < eps );
}
