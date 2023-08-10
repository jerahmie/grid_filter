#include <iostream>
#include <vector>
#include <algorithm>
#include <catch2/catch_test_macros.hpp>
#include "kdtree_node.h"
#include "kdtree_util.h"
#include "mpas_file.h"

TEST_CASE("Test catch2 setup.", "[test_kdtree_util]") {
  REQUIRE(42 == 42);
}

std::vector<nodeData> test_points10 {{0.50, 0.08, 0},
                                    {0.20, 0.12, 1},
                                    {0.87, 1.00, 2},
                                    {0.69, 0.11, 3},
                                    {0.29, 0.49, 4},
                                    {0.96, 0.16, 5},
                                    {0.38, 0.32, 6},
                                    {0.39, 0.55, 7},
                                    {0.14, 0.84, 8},
                                    {0.98, 0.53, 9}};

TEST_CASE("Test kdtree_util compare_lat.", "[test_kdtree_util]") {
  REQUIRE(test_points10.size() == 10);
  std::sort(test_points10.begin(), test_points10.end(), compare_lat);
  double lat_prev = test_points10[0].lat;
  for (auto &pt : test_points10) {
    REQUIRE(pt.lat >= lat_prev);
    lat_prev = pt.lat;
  }
}

TEST_CASE("Test kdtree_util compare_lon.", "[test_kdtree_util]") {
  REQUIRE(test_points10.size() == 10);
  std::sort(test_points10.begin(), test_points10.end(), compare_lon);
  double lon_prev = test_points10[0].lon;
  for (auto &pt : test_points10) {
    REQUIRE(pt.lon >= lon_prev);
    lon_prev = pt.lon;
  }
}
TEST_CASE("Test median point helper function.", "[test_kdtree_util]") {
  const std::vector<nodeData> node_data0 { }; // empty
  const std::vector<nodeData> node_data1 { {0.12, 3.45, 0}};
  const std::vector<nodeData> node_data2 { {0.12, 3.45, 0},
                                           {0.24, 6.8, 1} };
  const std::vector<nodeData> node_data3 { {0.12, 3.45, 0},
                                           {0.24, 6.8, 1},
                                           {0.46, 5.3, 2} };
  const std::vector<nodeData> node_data4 { {0.12, 3.45, 0},
                                           {0.24, 6.8, 1},
                                           {0.46, 5.3, 2},
                                           {0.58, 7.1, 3} };
  int nd_len = node_data1.size();
  double half_len_float = nd_len/2.0;
  int half_len_int = int(half_len_float);
  std::cout << "<-> " << std::get<1>(median_point_id(node_data1)) << '\n';
  REQUIRE(std::get<0>(median_point_id(node_data1)) == node_data1[0]);
  REQUIRE(std::get<1>(median_point_id(node_data1)) == 0);
  REQUIRE(std::get<1>(median_point_id(node_data2)) == 1);
  REQUIRE(std::get<1>(median_point_id(node_data3)) == 1);
  REQUIRE(std::get<1>(median_point_id(node_data4)) == 2);
}
