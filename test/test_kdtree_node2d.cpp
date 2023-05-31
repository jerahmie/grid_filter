#include <catch2/catch_test_macros.hpp>
#include "kdtree_node.h"
//#include "kdtree.h"


TEST_CASE("TEST Catch2 Setup", "[test_kdtree_node]") {
  CHECK(42 == 42);
}

TEST_CASE("CREATE Test Node Data", "[test_kdtree_node") {
  nodeData nd{0.12, 3.45, 8};
  REQUIRE(nd.cell_index == 8);
  REQUIRE(nd.lat == 0.12);
  REQUIRE(nd.lon == 3.45);
}

TEST_CASE("Create KDTree node.", "[test_kdtree_node]") {
  nodeData nd{0.12, 3.45, 1};
  KDTreeNode2D kd2 {NULL, NULL, nd};
  REQUIRE(kd2.getLeft() == NULL);
  REQUIRE(kd2.getRight() == NULL);
  
}
