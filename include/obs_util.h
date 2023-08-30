/*
 * file - obs_util.h
 * Utilities to read and preprocess observation data.
 */

#pragma once
#include <vector>
#include <string>
#include <typeinfo>
#include <hdf5.h>
//#include <H5Cpp.h>
//#include <H5Exception.h>
#include "kdtree_util.h"

std::vector<float> read_h5data(std::string&, std::string, std::string);

std::vector<point2D> read_obs_points(std::string&);

template <typename T>
int write_h5data_1d(std::string &filename, std::string &groupname,
                  std::string &datasetname,  std::vector<T> &data) {
  
//  try {
    
//    H5::H5File h5file = H5::H5File(filename, H5F_ACC_TRUNC);
//    H5::Group group = h5file.createGroup(groupname.c_str());
//    const hsize_t dims[1] {data.size()};
//    H5::DataSpace dataspace(1, dims);
//    
//    H5::DataSet dataset = group.createDataSet(datasetname,
//                                              H5::PredType::NATIVE_INT,
//                                              dataspace);
//    dataset.write(data.data(), H5::PredType::NATIVE_INT);
//    dataspace.close();
//    dataset.close(); 
//    h5file.close();
//  }
//  // catch failure due to H5File operations
//  catch ( H5::FileIException error ) {
//    error.printErrorStack();
//    return -1;
//}
//
//  // catch failure due to DataSet operations
//  catch ( H5::DataSetIException error ) { 
//    error.printErrorStack();
//    return -1;
//    }
//  // catch failure due to DataSpace operations
//  catch ( H5::DataSpaceIException error ){
//    error.printErrorStack();
//    return -1;
//}
//
    return 0;
}

