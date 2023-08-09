#include <iostream>
#include <vector>
#include <string>
#include <stdexcept>
#include <catch2/catch_test_macros.hpp>
#include "mpas_util.h"
#include "kdtree_node.h"


std::vector<float> lats{ 0.77, 0.51, 0.82, 0.89, 0.53,
                         0.34, 0.67, 0.99, 0.92, 0.15 };

std::vector<float> lons{ 0.69, 0.31, 0.90, 0.75, 0.02,
                         0.18, 0.17, 0.09, 0.90, 0.39 };
float eps = 0.0001; // a small number for comparison

TEST_CASE("Test_mpas_util catch2 setup.", "[test_mpas_util]") {
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
