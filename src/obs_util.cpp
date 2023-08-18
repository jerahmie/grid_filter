/*
 * file - obs_util.cpp
 * Read and preprocess observations.
 */

#include <vector>
#include <string>
#include "H5Cpp.h"
#include "kdtree_util.h"
#include "obs_util.h"

// Read 1D data from hdf5 file.
std::vector<float> read_h5data(std::string &filename,
                               std::string group,
                               std::string dataset) {
  H5::H5File h5file = H5::H5File(filename, H5F_ACC_RDONLY);
  H5::Group hgroup = h5file.openGroup(group);
  H5::DataSet hdataset = hgroup.openDataSet(dataset);
  H5::DataSpace dataspace = hdataset.getSpace();
  int rank = dataspace.getSimpleExtentNdims();
  hsize_t dims_out[rank];
  int ndims = dataspace.getSimpleExtentDims( dims_out, NULL );
  int nelements = dims_out[0];

  /* Define memory dataspace. */
  hsize_t dimsm[1];
  dimsm[0] = nelements;
  H5::DataSpace memspace ( 1, dimsm );

  H5T_class_t type_class = hdataset.getTypeClass();
  float data_buf[nelements];
  for (int i=0; i<nelements; i++ ) { data_buf[i] = 0; }
  hdataset.read( data_buf, H5::PredType::NATIVE_FLOAT, memspace, dataspace);
  std::vector<float> data_out;
  data_out.assign(data_buf, data_buf+nelements);

  return data_out;
}

// Read observation points from data file.
std::vector<point2D> read_obs_points(std::string &filename) {
  std::vector<float> latitude = read_h5data(filename, "/MetaData", "latitude");
  std::vector<float> longitude = read_h5data(filename, "/MetaData", "longitude");
  std::vector<point2D> obs_points;
  int nelements = latitude.size();
  for (int i=0; i<nelements; i++) {
    obs_points.push_back(point2D {latitude[i], longitude[i]} );
  }
  return obs_points;
}
