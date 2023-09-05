/*
 * file - obs_util.cpp
 * Read and preprocess observations.
 */
#include <iostream>
#include <vector>
#include <string>
#include <hdf5.h>
#include "kdtree_util.h"
#include "obs_util.h"

// Read 1D data from hdf5 file.
std::vector<float> read_h5data(std::string &filename,
                               std::string group,
                               std::string dataset) {
  int status = 0;
  // Gather observation file metadata.
  // TODO: check return types and add error handling.
  hid_t file_id = H5Fopen(filename.c_str(), H5F_ACC_RDONLY, H5P_DEFAULT); 
  hid_t group_id = H5Gopen2(file_id, group.c_str(), H5P_DEFAULT);
  hid_t dataset_id = H5Dopen2(group_id, dataset.c_str(), H5P_DEFAULT);
  hid_t dataspace_id = H5Dget_space(dataset_id);
  int rank = H5Sget_simple_extent_ndims(dataspace_id);

  // Gather dataset metadata.
  hsize_t dims_out[rank];
  int ndims = H5Sget_simple_extent_dims(dataspace_id, dims_out, NULL);
  H5S_class_t type_class = H5Sget_simple_extent_type(dataspace_id);
  hssize_t nelements = H5Sget_simple_extent_npoints(dataspace_id);
   
  // Define memory dataspace and read data.
  hsize_t dimsm[1];
  dimsm[0] = dims_out[0];
  float data_buf[nelements];
  for (int i=0; i<nelements; i++ ) { data_buf[i] = 0; }
  status = H5Dread(dataset_id, H5T_NATIVE_FLOAT, H5S_ALL, H5S_ALL, H5P_DEFAULT, data_buf);
  std::vector<float> data;
  data.assign(data_buf, data_buf+nelements);

  H5Dclose(dataspace_id);
  H5Dclose(dataset_id);
  H5Gclose(group_id);
  H5Fclose(file_id);

  return data;
}

// Save the mask file to a hdf5 file.
int write_mask(std::string &filename, std::string& group,
               std::string &dataset, std::vector<int> &mask) {
  hid_t file_id = H5Fcreate(filename.c_str(), H5F_ACC_TRUNC, H5P_DEFAULT, H5P_DEFAULT);
  hid_t group_id = H5Gcreate2(file_id, group.c_str(), H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
  hsize_t dims[1];
  dims[0] = mask.size();
  hid_t dataspace_id = H5Screate_simple(1, dims, NULL);
  hid_t dataset_id = H5Dcreate2(group_id, dataset.c_str(), H5T_NATIVE_INT, dataspace_id, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);

  int status = H5Dwrite(dataset_id, H5T_NATIVE_INT, H5S_ALL, H5S_ALL, H5P_DEFAULT, mask.data());

  H5Dclose(dataset_id);
  H5Sclose(dataspace_id);
  H5Gclose(group_id);
  H5Fclose(file_id);
  return status;
}

// Read observation points from data file.
std::vector<point2D> read_obs_points(std::string &filename) {
  std::vector<float> latitude = read_h5data(filename, "/MetaData", "latitude");
  std::vector<float> longitude = read_h5data(filename, "/MetaData", "longitude");
  for (int i=0; i<longitude.size(); i++) {
    if (longitude.at(i) < 0.0) { longitude.at(i) += 360.0; }
  }
  std::vector<point2D> obs_points;
  int nelements = latitude.size();
  for (int i=0; i<nelements; i++) {
    obs_points.push_back(point2D {latitude[i], longitude[i]} );
  }
  return obs_points;
}
