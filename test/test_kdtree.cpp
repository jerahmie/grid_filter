#include <iostream>
#include <vector>
#include <catch2/catch_test_macros.hpp>
#include "kdtree_node.h"
#include "kdtree.h"


TEST_CASE("TEST Catch2 Setup", "[test_kdtree]") {
  CHECK(42 == 42);
}

TEST_CASE("Two node tree with left child.", "[test_kdtree]") {
  std::vector<nodeData> node_data { {0.12, 3.45, 0},
    {0.24, 6.8, 1} };
  REQUIRE(node_data[0].cell_index == 0);
  REQUIRE(node_data[1].cell_index == 1);
}

TEST_CASE("Sort list of points along specified dimension.", "[test_kdtree]") {
  std::vector<nodeData> node_data { {0.96, 0.72, 0},
                                    {0.41, 0.67, 1},
                                    {0.3, 0.38, 2},
                                    {0.58, 0.54, 3},
                                    {0.47, 0.82, 4},
                                    {0.61, 0.61, 5},
                                    {0.25, 0.35, 6},
                                    {0.07, 0.39, 7},
                                    {0.03, 0.84, 8},
                                    {0.81, 0.06, 9} };
  std::cout << node_data[0].cell_index << '\n'; 
}
