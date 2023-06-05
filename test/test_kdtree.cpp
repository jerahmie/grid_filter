#include <iostream>
#include <vector>
#include <tuple>
#include <catch2/catch_test_macros.hpp>
#include "kdtree_node.h"
#include "kdtree.h"


  std::vector<nodeData> node_data10 { {0.96, 0.72, 0},
                                      {0.41, 0.67, 1},
                                      {0.3, 0.38, 2},
                                      {0.58, 0.54, 3},
                                      {0.47, 0.82, 4},
                                      {0.61, 0.61, 5},
                                      {0.25, 0.35, 6},
                                      {0.07, 0.39, 7},
                                      {0.03, 0.84, 8},
                                      {0.81, 0.06, 9} };
TEST_CASE("TEST Catch2 Setup", "[test_kdtree]") {
  CHECK(42 == 42);
}

TEST_CASE("Two node tree with left child.", "[test_kdtree]") {
  std::vector<nodeData> node_data { {0.12, 3.45, 0},
    {0.24, 6.8, 1} };
  REQUIRE(node_data[0].cell_index == 0);
  REQUIRE(node_data[1].cell_index == 1);

}

TEST_CASE("Test median point helper function.", "[test_kdtree]") {
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
//  REQUIRE(median_point_id(node_data0)) == 0);
  REQUIRE(std::get<0>(median_point_id(node_data1)) == node_data1[0]);
  REQUIRE(std::get<1>(median_point_id(node_data1)) == 0);
  REQUIRE(std::get<1>(median_point_id(node_data2)) == 1);
  REQUIRE(std::get<1>(median_point_id(node_data3)) == 1);
  REQUIRE(std::get<1>(median_point_id(node_data4)) == 2);

}


