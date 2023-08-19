/*
 * MPAS Grid data loader.
 */
#include <iostream>
#include <vector>
#include <netcdf>
#include "mpas_file.h"

// MPSFile contructor with netcdf filename.
MPASFile::MPASFile(std::string &filename) {
  if (retval = nc_open(filename.c_str(), NC_NOWRITE, &ncid)) { mperr(retval); }
}

MPASFile::~MPASFile() {
  if (retval = nc_close(ncid)) { mperr(retval); }
}

// Print netcdf error string.
void MPASFile::mperr(int e) {
  std::cout << "Error: " << nc_strerror(e) << '\n';
}

// Read a dimension value by name
int MPASFile::read_dim(std::string dimname) {
 int dimid = 0;
 size_t dimval = 0;
 if (retval = nc_inq_dimid(ncid, dimname.c_str(), &dimid)) { mperr(retval); }
 if (retval = nc_inq_dimlen(ncid, dimid, &dimval)) { mperr(retval); }

 return static_cast<int>(dimval);
}

// TODO: Template read_var_1d_float and read_var_1d_int to a single function
// Return vector of float data.
std::vector<float> MPASFile::read_var_1d_float(std::string varname, int n) {
  int varid;
  float data[n];
  if (retval = nc_inq_varid(ncid, varname.c_str(), &varid)) { mperr(retval); }
  if (retval = nc_get_var_float(ncid, varid, &data[0])) { mperr(retval); }
  std::vector<float> var_1d(data, data+n);

  return var_1d;
}

// Return vector of integer data.
std::vector<int> MPASFile::read_var_1d_int(std::string varname, int n) {
  int varid;
  int data[n];
  if (retval = nc_inq_varid(ncid, varname.c_str(), &varid)) { mperr(retval); }
  if (retval = nc_get_var_int(ncid, varid, &data[0])) { mperr(retval); }
  std::vector<int> var_1d(data, data+n);

  return var_1d;
}
