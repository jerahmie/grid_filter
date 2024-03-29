#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <unistd.h>
#include <linux/limits.h>
#include <catch2/catch_test_macros.hpp>
#include "mpas_file.h"
#include "mpas_util.h"

// relative location of MPAS Regional Static file.
#define STATIC_FILE "/../../test/python_tests/Manitowoc.static.nc"

TEST_CASE("Test catch2 setup.", "[test_load_regional_data]") {
  REQUIRE(42 == 42);
}

TEST_CASE("Test MPAS_FILE exists.", "[test_load_regional_data]"){
  // Ensure the test static file can be found, relative to the 
  // project test directory.
  char curr_dir[PATH_MAX];
  char* result = getcwd(curr_dir, sizeof(curr_dir));
  REQUIRE(result != NULL);
  std::string mpas_file(curr_dir);
  mpas_file += STATIC_FILE;
  std::cout << "mpas_file: " << mpas_file << '\n';
  std::ifstream ifs; 
  ifs.open(mpas_file, std::ifstream::in);
  REQUIRE(ifs.is_open() == true );
  ifs.close();
}

TEST_CASE("Test read lats and lons.", "[test_load_regional_data]") {
  char curr_dir[PATH_MAX];
  getcwd(curr_dir, sizeof(curr_dir));

  //MPAS Regional Static file location.
  std::string mpas_loc (curr_dir);
  mpas_loc += STATIC_FILE;
  MPASFile mpf = MPASFile(mpas_loc);
  int ncells = mpf.read_dim("nCells");
  REQUIRE(ncells == 441);
  std::vector<float> lats_radians = mpf.read_var_1d_float("latCell", ncells);
  std::vector<float> lons_radians = mpf.read_var_1d_float("lonCell", ncells);
  std::vector<int> bdy_cells = mpf.read_var_1d_int("bdyMaskCell", ncells); 
  REQUIRE(bdy_cells.size() == (long unsigned int)ncells);
  for (auto bc : bdy_cells) {
    REQUIRE(((bc >= 0) && ( bc <= 7)));
  }
}
