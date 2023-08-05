#include <iostream>
#include <vector>
#include <tuple>
#include <memory>
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

std::vector<std::unique_ptr<nodeData>> node_data_up; 


 
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
  REQUIRE(std::get<0>(median_point_id(node_data1)) == node_data1[0]);
  REQUIRE(std::get<1>(median_point_id(node_data1)) == 0);
  REQUIRE(std::get<1>(median_point_id(node_data2)) == 1);
  REQUIRE(std::get<1>(median_point_id(node_data3)) == 1);
  REQUIRE(std::get<1>(median_point_id(node_data4)) == 2);
}

TEST_CASE("Test small kdtree construction.", "[test_kdtree]") {
  // Test small KD-tree construction.
  // Single node tree
  int med_id = std::get<1>(median_point_id(node_data10));
  std::cout << "med_id: " << med_id << '\n';
  KDTreeNode2D kd2d_root {NULL, NULL, std::make_shared<nodeData>(node_data10[med_id])};
  std::unique_ptr<KDTreeNode2D> kd2d_p = std::make_unique<KDTreeNode2D>(kd2d_root);
  REQUIRE(kd2d_root.getLeft() == NULL);
  REQUIRE(kd2d_root.getRight() == NULL);
  REQUIRE(kd2d_p->getData()->cell_index == 5);
}

TEST_CASE("Test construction of kd tree.", "[test_kdtree]") {
  // tree with single point
 // std::vector<nodeData> pts0 { {0.0, 1.1, 0} };
 // std::vector<nodeData> pts1 { {1.2, 3.4, 1} };
  //auto pts0_p = std::make_shared<std::vector<nodeData>>(pts0);
//  KDTreeNode2D kd2d_0 = build_tree(pts0, pts0.begin(), pts0.end(), 0); 
//  REQUIRE(kd2d_0.getLeft() == NULL);
//  REQUIRE(kd2d_0.getRight() == NULL);
//  REQUIRE((*kd2d_0.getData()).cell_index == 0);
//  KDTreeNode2D kd2d_1 = build_tree(pts1, pts1.begin(), pts1.end(), 0);
//  REQUIRE(kd2d_1.getLeft() == NULL);
//  REQUIRE(kd2d_1.getRight() == NULL);
//  REQUIRE((*kd2d_1.getData()).cell_index == 1);

  std::vector<nodeData> pts { {0.0, 1.1, 0}, {1.1, -1.0, 1}, {2.2, -1.2, 2}, {3.3, 4.4, 3}};
  auto pts_p = std::make_shared<std::vector<nodeData>>(pts); 
  REQUIRE(pts.size() == 4);
  std::unique_ptr<KDTreeNode2D> kd2d = std::make_unique<KDTreeNode2D>(build_tree(pts, pts.begin(), pts.end(), 0));
  std::cout << "[test_kdtree] pts.begin(): " << (*pts.begin()) << " pts.end(): " << *(pts.end()-1) << '\n';
  REQUIRE(kd2d->getData()->cell_index == 2);
  REQUIRE(kd2d->getLeft()->getData()->cell_index == 0);
  REQUIRE(kd2d->getLeft()->getLeft()->getData()->cell_index == 1);
  REQUIRE(kd2d->getLeft()->getRight() == NULL);
  REQUIRE(kd2d->getRight()->getData()->cell_index == 3);
  REQUIRE(kd2d->getRight()->getRight() == NULL);
  REQUIRE(kd2d->getRight()->getLeft() == NULL);
}

TEST_CASE("Test build_tree.", "[test_kdtree]") {
  std::vector<nodeData> pts1 { {0.0, 1.1, 0} };
  KDTreeNode2D kd2d_pts1 = build_tree(pts1, pts1.begin(), pts1.end(), 0); 
  REQUIRE(kd2d_pts1.getLeft() == NULL);
  REQUIRE(kd2d_pts1.getRight() == NULL);
  REQUIRE((*kd2d_pts1.getData()).cell_index == 0);

  std::vector<nodeData> pts4 { {0.0, 1.1, 0}, {1.1, -1.0, 1}, {2.2, -1.2, 2}, {3.3, 4.4, 3}};
  KDTreeNode2D kd2d_pts4 = build_tree(pts4, pts4.begin(), pts4.end(), 0); 
  REQUIRE(kd2d_pts4.getLeft() == NULL);
  REQUIRE(kd2d_pts4.getRight() == NULL);
  REQUIRE((*kd2d_pts4.getData()).cell_index == 2);
}

