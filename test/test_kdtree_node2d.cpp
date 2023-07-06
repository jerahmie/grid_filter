#include <iostream>
#include <algorithm>
#include <catch2/catch_test_macros.hpp>
#include "kdtree_node.h"

std::vector<nodeData> node_vec3{{0.12, 3.45, 2},
                                {0.24, 6.8, 1},
                                {0.35, 4.66, 0}};

std::vector<nodeData> node_vec20{{0.56, 1.71, 0},
                                 {0.45, 0.32, 1},
                                 {0.73, 0.19, 2},
                                 {0.09, 1.65, 3},
                                 {0.67, 0.03, 4},
                                 {0.32, 0.87, 5},
                                 {0.56, 1.26, 6},
                                 {0.0, 1.6, 7},
                                 {0.17, 1.82, 8},
                                 {0.56, 1.07, 9},
                                 {0.37, 0.11, 10},
                                 {0.3, 0.86, 11},
                                 {0.05, 1.59, 12},
                                 {0.47, 1.56, 13},
                                 {0.91, 0.18, 14},
                                 {0.06, 1.35, 15},
                                 {0.84, 0.43, 16},
                                 {0.36, 0.46, 17},
                                 {0.5, 1.05, 18},
                                 {0.59, 1.77, 19}};


TEST_CASE("TEST Catch2 Setup", "[test_kdtree_node]") {
  // Test the unit testing environment.  (This should always pass.)
  CHECK(42 == 42);
}

TEST_CASE("CREATE Test Node Data", "[test_kdtree_node]") {
  // Create a single node data struct and verify all members are visible.
  const nodeData nd{0.12, 3.45, 8};
  REQUIRE(nd.cell_index == 8);
  REQUIRE(nd.lat == 0.12);
  REQUIRE(nd.lon == 3.45);
}

//TEST_CASE("Create KDTree node.", "[test_kdtree_node]") {
//  // Create a 2D KDTree leaf node containing sample data.
//  const nodeData nd{0.12, 3.45, 1};
//  KDTreeNode2D kd2 {NULL, NULL, nd};
//  REQUIRE(kd2.getLeft() == NULL);
//  REQUIRE(kd2.getRight() == NULL);
//  REQUIRE(kd2.getData().cell_index == 1); 
//  REQUIRE(kd2.getData().lat == 0.12);
//  REQUIRE(kd2.getData().lon == 3.45);
//}
//
//TEST_CASE("Split vector by given dimension.", "[test_kdtree_node]") {
//  // Test split sorted array by median
//  int node_vec3_mid = node_vec3.size()/2;
//  REQUIRE(node_vec3_mid == 1);
//  int node_vec20_mid = node_vec20.size()/2;
//  REQUIRE(node_vec20_mid == 10);
//  std::sort(node_vec3.begin(), node_vec3.end(), compare_node_lat);
//  // sub vector from sorted vectornode_vec3
//  nodeData mid = node_vec3.at(node_vec3_mid);
//  REQUIRE(mid.cell_index == 1);
//  std::vector<nodeData>::const_iterator left_begin = node_vec3.begin();
//  std::vector<nodeData>::const_iterator left_end = node_vec3.begin() + node_vec3_mid;
//  std::vector<nodeData> left_data(left_begin, left_end);
//  REQUIRE(left_data.size() == 1);
//  REQUIRE(left_data.at(0).cell_index == 2);
//  std::vector<nodeData>::const_iterator right_begin = node_vec3.begin() + node_vec3_mid + 1;
//  std::vector<nodeData>::const_iterator right_end = node_vec3.end();
//  std::vector<nodeData> right_data(right_begin, right_end);
//  REQUIRE(right_data.size() == 1);
//  REQUIRE(right_data.at(0).cell_index == 0);
//}
//
//TEST_CASE("Test sorting list of node data.", "[test_kdtree_node]") {
//  // Sort vector of node data by longitude
//  std::sort(node_vec20.begin(), node_vec20.end(), compare_node_lon); 
//  std::vector<nodeData>::iterator iter1 = node_vec20.begin();
//  for (iter1; iter1 < node_vec20.end()-1; iter1++) {
//    auto next_item = iter1+1;
//    std::cout << (*iter1).lon << " " << (*next_item).lon << '\n';
//    REQUIRE((*iter1).lon <= (*next_item).lon);
//  }
//  // Sort vector of node data by latitude
//  std::sort(node_vec20.begin(), node_vec20.end(), compare_node_lat); 
//  std::vector<nodeData>::iterator iter2 = node_vec20.begin();
//  for (iter2; iter2 < node_vec20.end()-1; iter2++) {
//    auto next_item = iter2+1;
//    std::cout << (*iter2).lat << " " << (*next_item).lat << '\n';
//    REQUIRE((*iter2).lat <= (*next_item).lat);
//  }
//}
//TEST_CASE("Test node compare of nodes via == operator", "[test_kdtree_node]") {
//  const nodeData test_node1{0.35, 4.66, 0};
//  const nodeData test_node2{0.35, 4.66, 0};
//  REQUIRE(test_node1 == test_node2);
//  REQUIRE(test_node1 != node_vec3[0]);
//  REQUIRE(test_node1 != node_vec3[1]);
//  REQUIRE(test_node1 == node_vec3[2]);
//};
