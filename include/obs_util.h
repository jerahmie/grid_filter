/*
 * file - obs_util.h
 */

#pragma once
#include <vector>
#include <string>
#include <typeinfo>
#include "H5Cpp.h"
#include "kdtree_util.h"


std::vector<float> read_h5data(std::string&, std::string, std::string);

std::vector<point2D> read_obs_points(std::string&);

template <typename T>
void write_h5data_1d(std::string &filename, std::string &groupname,
                  std::string &datasetname,  std::vector<T> &data) {
  if constexpr (std::is_same<T, int>::value) {
    auto data_type = H5::PredType::NATIVE_INT;
    std::cout << "Data is of type 'int' \n";
  } else if constexpr (std::is_same<T, float>::value) {
    auto data_type = H5::PredType::NATIVE_FLOAT;
    std::cout << "Data is of type 'float' \n";
  } else if constexpr (std::is_same<T, double>::value) {
    auto data_type = H5::PredType::NATIVE_DOUBLE; 
    std::cout << "Data is of type 'double' \n";
  } else {
    std::cout << "Data type is unknown.\n";
  }
  //try {
   H5::H5File h5file = H5::H5File(filename, H5F_ACC_TRUNC);
   H5::Group group = h5file.createGroup(groupname.c_str());
   const hsize_t dims[1] {data.size()};
   H5::DataSpace dataspace(1, dims);
   H5::DataSet dataset = group.createDataSet(datasetname, H5::PredType::NATIVE_INT, dataspace);
   dataset.write(data.data(), H5::PredType::NATIVE_INT);
   dataspace.close();
   dataset.close(); 
   h5file.close();
  // }
}

