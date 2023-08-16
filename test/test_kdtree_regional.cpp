#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include <unistd.h>
#include <linux/limits.h>
#include <catch2/catch_test_macros.hpp>
#include "mpas_file.h"
#include "mpas_util.h"
#include "kdtree_node.h"
#include "kdtree_util.h"
#include "kdtree.h"

double uniform(double min, double max){
  //double mean = (max+min)/2.0;
  double urange = (max-min);
  return min+urange*((double)rand())/((double)RAND_MAX);
}

int nearest_bf(point2D &qpt, std::vector<nodeData> &ptsi) {
  double w = 1.0e100;
  double w_pt = 0.0;
  int min_index = 0;
  for (auto &p : ptsi) {
    point2D pt {p.lat, p.lon};
    w_pt = euclidean_2d_distance_sq(qpt, pt);
    if (w_pt < w) {
      min_index = p.cell_index;
      w = w_pt;
    }
  }
  return min_index;
}

TEST_CASE("Test Catch2 Setup", "[test_kdtree_regional]") {
  REQUIRE(42 == 42);
}

TEST_CASE("Test Internal Points", "[test_kdtree_regional]") {
  // Test nearest points within a 2D KD-tree.
  std::string static_file = "/../../test/python_tests/Manitowoc.static.nc";
  char curr_dir[PATH_MAX];
  char* result = getcwd(curr_dir, sizeof(curr_dir));
  std::string mpas_loc {curr_dir};
  mpas_loc += static_file;
  MPASFile mpf = MPASFile(mpas_loc);
  int ncells = mpf.read_dim("nCells");
  std::vector<float> lats = mpf.read_var_1d_float("latCell", ncells);
  std::vector<float> lons = mpf.read_var_1d_float("lonCell", ncells);
  std::vector<nodeData> ptsi = merge_lat_lon(lats, lons);
  REQUIRE(ptsi.size() == 441);
  KDTree kd2d = KDTree(ptsi);
  std::vector<point2D> qpts { {0.75, 4.7}, {0.69, 4.8}, {0.85, 4.65} };
  REQUIRE(abs(qpts[0].lon - 4.7) < 0.0001);
  for (auto &qpt : qpts) {
    int min_id_bf = nearest_bf(qpt, ptsi);
    int min_id_kd = kd2d.find_nearest_cell_id(qpt.lat, qpt.lon);
    REQUIRE(min_id_bf == min_id_kd);
  }
}

TEST_CASE("Test Random Points", "[test_kdtree_regional]") {
  // Test nearest points within a 2D KD-tree.
  std::string static_file = "/../../test/python_tests/Manitowoc.static.nc";
  char curr_dir[PATH_MAX];
  char* result = getcwd(curr_dir, sizeof(curr_dir));
  std::string mpas_loc {curr_dir};
  mpas_loc += static_file;
  MPASFile mpf = MPASFile(mpas_loc);
  int ncells = mpf.read_dim("nCells");
  std::vector<float> lats = mpf.read_var_1d_float("latCell", ncells);
  std::vector<float> lons = mpf.read_var_1d_float("lonCell", ncells);
  std::vector<nodeData> ptsi = merge_lat_lon(lats, lons);
  REQUIRE(ptsi.size() == 441);
  KDTree kd2d = KDTree(ptsi);
  //std::vector<point2D> qpts { {0.75, 4.7}, {0.69, 4.8}, {0.85, 4.65} };
  std::vector<point2D> qpts;
  for (int i=0; i<1000; i++) {
    qpts.push_back({uniform(0.5, 0.9), uniform(4.3, 5.0)});
  }
  for (auto &qpt : qpts) {
    std::cout << qpt.lat << ", " << qpt.lon << '\n';
    int min_id_bf = nearest_bf(qpt, ptsi);
    int min_id_kd = kd2d.find_nearest_cell_id(qpt.lat, qpt.lon);
    REQUIRE(min_id_bf == min_id_kd);
  }
}
