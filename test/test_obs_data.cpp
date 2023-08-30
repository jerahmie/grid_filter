#include <iostream>
#include <vector>
#include <unistd.h>
#include <fstream>
#include <linux/limits.h>
#include <catch2/catch_test_macros.hpp>
#include "hdf5.h"
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

  // Gather data from observation file.
  std::string obs_filename(curr_dir);
  obs_filename += OBS_FILE_REL;
  hid_t file_id = H5Fopen(obs_filename.c_str(), H5F_ACC_RDONLY, H5P_DEFAULT);
  hid_t group_id = H5Gopen2(file_id, GROUPNAME.c_str(), H5P_DEFAULT);
  hid_t dset_id = H5Dopen2(group_id, "longitude", H5P_DEFAULT);
  hid_t file_type = H5Dget_type(dset_id);
  hid_t dspace_id = H5Dget_space(dset_id);
  int rank = H5Sget_simple_extent_ndims(dspace_id);

  hsize_t dims_out[rank];
  int ndims = H5Sget_simple_extent_dims(dspace_id, dims_out, NULL);
  H5S_class_t type_class = H5Sget_simple_extent_type(dspace_id); 
  hssize_t nelements = H5Sget_simple_extent_npoints(dspace_id); 
  
  // Define memory dataspace and read data into buffer.
  hsize_t dimsm[1];
  dimsm[0] = dims_out[0];
  std::cout << "dimsm: " << dims_out[0] <<'\n';
  float data_out [nelements];
  int status = H5Dread(dset_id, H5T_NATIVE_FLOAT, H5S_ALL, H5S_ALL, H5P_DEFAULT, data_out);
  REQUIRE(status == 0);
  REQUIRE((int)type_class == (int)H5T_FLOAT);
  REQUIRE(rank == 1);
  REQUIRE(nelements == 287290);
  for (int i=0; i<nelements; i++) {
    data_out[i] = 0.0;
  }
  float data_min = data_out[0];
  int min_index = 0;
  float data_max = data_out[0];
  for (int i=0; i<nelements; i++) {
    if (data_out[i] < data_min) { data_min = data_out[i]; min_index = i; }
    if (data_out[i] > data_max) { data_max = data_out[i]; }
  }
  REQUIRE( data_min >= 0.0 );
  REQUIRE( data_max <= 360.0 );
  H5Dclose(dspace_id);
  H5Dclose(dset_id);
  H5Gclose(group_id);
  H5Fclose(file_id);
  }

TEST_CASE("Test obs_util read_h5data.", "[test_obs_data]") {
  // Read hdf5 latitude/longitude data using convenience function.
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

