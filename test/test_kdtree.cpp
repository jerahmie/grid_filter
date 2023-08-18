#include <iostream>
#include <vector>
#include <tuple>
#include <memory>
#include <string>
#include <unistd.h>
#include <linux/limits.h>
#include <catch2/catch_test_macros.hpp>
#include "kdtree_node.h"
#include "kdtree_util.h"
#include "build_tree.h"
#include "kdtree.h"
#include "mpas_file.h"
#include "mpas_util.h"

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


 
TEST_CASE("Test Catch2 setup.", "[test_kdtree]") {
  CHECK(42 == 42);
}

TEST_CASE("Two node tree with left child.", "[test_kdtree]") {
  std::vector<nodeData> node_data { {0.12, 3.45, 0},
                                    {0.24, 6.8, 1} };
  REQUIRE(node_data[0].cell_index == 0);
  REQUIRE(node_data[1].cell_index == 1);
}

TEST_CASE("Test small tree verification.", "[test_kdtree]") {
  std::vector<nodeData> nd4 { {0.0,  1.1, 0},
                              {1.1, -1.0, 1},
                              {2.2, -1.1, 2},
                              {3.3,  4.4, 3} };
  std::cout << "Before build_tree: begin: " <<  *(nd4.begin()) << ", end: " << *(nd4.end()-1) << '\n';  
  KDTreeNode2D kd2d4 = build_tree(nd4, nd4.begin(), nd4.end(), 0);
  std::cout << " node: " << kd2d4.getData()->cell_index << '\n';
  std::cout << " left: " << kd2d4.getLeft()->getData()->cell_index << '\n';
  std::cout << "right: " << kd2d4.getRight()->getData()->cell_index << '\n';
  REQUIRE(kd2d4.getData()->cell_index == 1);
  REQUIRE(kd2d4.getLeft()->getData()->cell_index == 0);
  REQUIRE(kd2d4.getRight()->getData()->cell_index == 2);
  REQUIRE(kd2d4.getRight()->getRight()->getData()->cell_index == 3);
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
  std::vector<nodeData> pts0 { {0.0, 1.1, 0} };
  std::vector<nodeData> pts1 { {1.2, 3.4, 1} };
  //auto pts0_p = std::make_shared<std::vector<nodeData>>(pts0);
  KDTreeNode2D kd2d_0 = build_tree(pts0, pts0.begin(), pts0.end(), 0); 
  REQUIRE(kd2d_0.getLeft() == NULL);
  REQUIRE(kd2d_0.getRight() == NULL);
  REQUIRE((*kd2d_0.getData()).cell_index == 0);
  KDTreeNode2D kd2d_1 = build_tree(pts1, pts1.begin(), pts1.end(), 0);
  REQUIRE(kd2d_1.getLeft() == NULL);
  REQUIRE(kd2d_1.getRight() == NULL);
  REQUIRE((*kd2d_1.getData()).cell_index == 1);

  std::vector<nodeData> pts { {0.0, 1.1, 0}, {1.1, -1.0, 1}, {2.2, -1.2, 2}, {3.3, 4.4, 3}};
  auto pts_p = std::make_shared<std::vector<nodeData>>(pts); 
  REQUIRE(pts.size() == 4);
  std::unique_ptr<KDTreeNode2D> kd2d = std::make_unique<KDTreeNode2D>(build_tree(pts, pts.begin(), pts.end(), 0));
  std::cout << "[test_kdtree] pts.begin(): " << (*pts.begin()) << " pts.end(): " << *(pts.end()-1) << '\n';
  REQUIRE(kd2d->getData()->cell_index == 1);
  REQUIRE(kd2d->getLeft()->getData()->cell_index == 0);
  REQUIRE(kd2d->getLeft()->getRight() == NULL);
  REQUIRE(kd2d->getLeft()->getLeft() == NULL);
  REQUIRE(kd2d->getRight()->getData()->cell_index == 2);
  REQUIRE(kd2d->getRight()->getRight()->getData()->cell_index == 3);
}

TEST_CASE("Test balanced tree.", "[test_kdtree]") {
  std::vector<nodeData> pts { {4.4, 1.9, 0}, 
                              {4.2, -2.0, 1}, 
                               {-2.3, -2.3, 2},
                               {-2.1, -2.5, 3},
                               {-1.4, 2.5, 4},
                               {4.6, -4.2, 5},
                               {-4.0, 4.3, 6} };

  KDTreeNode2D kd = build_tree(pts, pts.begin(), pts.end(), 0);
  REQUIRE(kd.getData()->cell_index == 4);
  REQUIRE(kd.getLeft()->getData()->cell_index == 2);
  REQUIRE(kd.getRight()->getData()->cell_index == 1);
  REQUIRE(kd.getLeft()->getLeft()->getData()->cell_index == 3);
  REQUIRE(kd.getLeft()->getRight()->getData()->cell_index == 6);
  REQUIRE(kd.getRight()->getLeft()->getData()->cell_index == 5);
  REQUIRE(kd.getRight()->getRight()->getData()->cell_index == 0);
}

TEST_CASE("Test unbalanced tree.", "[test_kdtree]") {
  std::vector<nodeData> pts { {4.4, 1.9, 0}, 
                              {4.2, -2.0, 1}, 
                               {-2.3, -2.3, 2},
                               {-2.1, -2.5, 3},
                               {-1.4, 2.5, 4},
                               {4.6, -4.2, 5}};
  KDTreeNode2D kd = build_tree(pts, pts.begin(), pts.end(), 0);
  REQUIRE(kd.getData()->cell_index == 4);
  REQUIRE(kd.getLeft()->getData()->cell_index == 3);
  REQUIRE(kd.getRight()->getData()->cell_index == 1);
  REQUIRE(kd.getLeft()->getRight()->getData()->cell_index == 2);
  REQUIRE(kd.getRight()->getLeft()->getData()->cell_index == 5);
  REQUIRE(kd.getRight()->getRight()->getData()->cell_index == 0);
}

TEST_CASE("Test kdtree from file.", "[test_kdtree]") {
  std::string static_file = "/../../test/python_tests/Manitowoc.static.nc";
  char curr_dir[PATH_MAX];
  char* result = getcwd(curr_dir, sizeof(curr_dir));
  REQUIRE(result != NULL);
  std::string mpas_loc(curr_dir);
  mpas_loc += static_file;
  MPASFile mpf = MPASFile(mpas_loc);
  int ncells = mpf.read_dim("nCells");
  std::vector<float> lats_radians = mpf.read_var_1d_float("latCell", ncells);
  std::vector<float> lons_radians = mpf.read_var_1d_float("lonCell", ncells);
  std::vector<nodeData> ptsi = merge_lat_lon(lats_radians, lons_radians);
  std::unique_ptr<KDTreeNode2D> kd2d = std::make_unique<KDTreeNode2D>(build_tree(ptsi, ptsi.begin(), ptsi.end(), 0));
  std::cout << "root: " << kd2d->getData()->cell_index << 
            ", left: " << kd2d->getLeft()->getData()->cell_index << 
            ", right: " << kd2d->getRight()->getData()->cell_index << '\n';
  REQUIRE(kd2d->getData()->cell_index == 303); 
  REQUIRE(kd2d->getLeft()->getData()->cell_index == 155);
  REQUIRE(kd2d->getRight()->getData()->cell_index == 226);
}

TEST_CASE("KDTree Constructor","[test_kdtree]") {
  // Set MPAS Static File.
  std::string static_file = "/../../test/python_tests/Manitowoc.static.nc";
  char curr_dir[PATH_MAX];
  char* result = getcwd(curr_dir, sizeof(curr_dir));
  REQUIRE(result != NULL);
  std::string mpas_loc(curr_dir);
  mpas_loc += static_file;
  // Read MPAS Static file data and merge to create lat, lon, cell_index data.
  MPASFile mpf = MPASFile(mpas_loc);
  int ncells = mpf.read_dim("nCells");
  std::vector<float> lats_radians = mpf.read_var_1d_float("latCell", ncells);
  std::vector<float> lons_radians = mpf.read_var_1d_float("lonCell", ncells);
  std::vector<nodeData> ptsi = merge_lat_lon(lats_radians, lons_radians);
  
  KDTree kd2d = KDTree(ptsi);
  REQUIRE(kd2d.root.getData()->cell_index == 303);
  float qlat = 0.86;
  float qlon = 4.76;
  int np = kd2d.find_nearest_cell_id(qlat, qlon);
  REQUIRE(np == 226);
}

TEST_CASE("KDTree Constructor From File","[test_kdtree]") {
  // Set MPAS Static File.
  std::string static_file = "/../../test/python_tests/Manitowoc.static.nc";
  char curr_dir[PATH_MAX];
  char* result = getcwd(curr_dir, sizeof(curr_dir));
  REQUIRE(result != NULL);
  std::string mpas_loc(curr_dir);
  mpas_loc += static_file;
  
  KDTree kd2d = KDTree(mpas_loc);
  REQUIRE(kd2d.root.getData()->cell_index == 303);
  float qlat = 0.86*180.0/3.14159;
  float qlon = 4.76*180.0/3.14159;
  int np = kd2d.find_nearest_cell_id(qlat, qlon);
  REQUIRE(np == 226);
}
