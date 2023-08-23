#include <iostream>
#include <vector>
#include <unistd.h>
#include <fstream>
#include <linux/limits.h>
#include <catch2/catch_test_macros.hpp>
#include "H5Cpp.h"
#include "obs_util.h"

#define NELEMENTS 287290
const std::string OBS_FILE_REL = "/../../test/python_tests/satwind_obs_2019050100.h5";
const std::string GROUPNAME = "/MetaData";


// convenience function to generate file path relative to current path
std::string gen_obs_file_path(const std::string &file_rel){
  char curr_dir[PATH_MAX];
  char* result = getcwd(curr_dir, sizeof(curr_dir));
  REQUIRE(result != NULL);
  std::string obs_file(curr_dir);
  obs_file += OBS_FILE_REL;
  return obs_file;
}


TEST_CASE("Test catch2 setup.", "[test_obs_data]") {
  REQUIRE(42 == 42);
}

TEST_CASE("Test read obs.", "[test_obs_data]") {
  char curr_dir[PATH_MAX];
  char* result = getcwd(curr_dir, sizeof(curr_dir));
  REQUIRE(result != NULL);
  std::string obs_file(curr_dir);
  obs_file += OBS_FILE_REL;
  std::cout << "obs_file: " << obs_file << '\n';
  std::ifstream ifs;
  ifs.open(obs_file, std::ifstream::in);
  REQUIRE( ifs.is_open() == true );
  ifs.close();
}

TEST_CASE("Test read obs lats and lons.", "[test_obs_data]") {
  // Test read of observations latitudes and longitudes.
  char curr_dir[PATH_MAX];
  getcwd(curr_dir, sizeof(curr_dir));

  // Obs file location.
  std::string obs_filename(curr_dir);
  obs_filename += OBS_FILE_REL;
  H5::H5File h5file = H5::H5File(obs_filename, H5F_ACC_RDONLY);
  H5::Group group = h5file.openGroup(GROUPNAME);
  H5::DataSet dataset = group.openDataSet("longitude"); 
  H5::DataSpace dataspace = dataset.getSpace();
  int rank = dataspace.getSimpleExtentNdims();
  hsize_t dims_out[rank];
  int ndims = dataspace.getSimpleExtentDims( dims_out, NULL);
  
  /* Define memory dataspace. */
  hsize_t dimsm[1];
  dimsm[0] = dims_out[0];
  H5::DataSpace memspace ( 1, dimsm );

  H5T_class_t type_class = dataset.getTypeClass();
  if (type_class == H5T_FLOAT) {
    auto ftype = dataset.getFloatType();
  }
  REQUIRE(type_class == H5T_FLOAT);
  auto lon_storage_size = dataset.getStorageSize();
  int nelements = dims_out[0];
  REQUIRE(rank == 1);
  REQUIRE(nelements == 287290);
  float data_out[nelements];
  for (int i=0; i<nelements; i++) {
    data_out[i] = 0.0;
  }
  dataset.read( data_out, H5::PredType::NATIVE_FLOAT, memspace, dataspace);
  float data_min = data_out[0];
  int min_index = 0;
  float data_max = data_out[0];
  for (int i=0; i<nelements; i++) {
    if (data_out[i] < data_min) { data_min = data_out[i]; min_index = i; }
    if (data_out[i] > data_max) { data_max = data_out[i]; }
  }
  REQUIRE( data_min >= 0.0 );
  REQUIRE( data_max <= 360.0 );
  }

TEST_CASE("Test obs_util read_h5data.", "[test_obs_data]") {
  std::string obs_file = gen_obs_file_path(OBS_FILE_REL);
  std::vector<float> latitude = read_h5data(obs_file, "/MetaData", "latitude");
  REQUIRE(latitude.size() == NELEMENTS);
  for (auto &i : latitude) {
    REQUIRE(((i>=-180.0) and (i<=180.0)));
  }
  std::vector<float> longitude = read_h5data(obs_file, "/MetaData", "latitude");
  REQUIRE(longitude.size() == NELEMENTS);
  for (auto &i : longitude) {
    REQUIRE(((i>=-180.0) and (i<=180.0)));
  }
}

TEST_CASE("Test read_obs_points.", "[test_obs_data]") {
  std::string obs_file_str = gen_obs_file_path(OBS_FILE_REL);
  std::vector<point2D> obs_points = read_obs_points(obs_file_str);
  REQUIRE(obs_points.size() == NELEMENTS);
}

