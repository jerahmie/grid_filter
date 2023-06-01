#include <vector>
#include <catch2/catch_test_macros.hpp>
#include "kdtree_node.h"
#include "kdtree.h"


TEST_CASE("TEST Catch2 Setup", "[test_kdtree]") {
  CHECK(42 == 42);
}

TEST_CASE("Two node tree with left child.", "[test_kdtree") {
  std::vector<nodeData> node_data { {0.12, 3.45, 0},
    {0.24, 6.8, 1} };
  REQUIRE(node_data[0].cell_index == 0);
  REQUIRE(node_data[1].cell_index == 1);
  
  
}
