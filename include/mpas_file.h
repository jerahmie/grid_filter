/*
 * mpas_grid.h
 *
 */

#pragma once

#include <vector>
#include <netcdf>
#include "kdtree_node.h"

class MPASFile {
  private:
  int ncid = 0;
  int retval = 0;
  void mperr(int);

  public:
  MPASFile(std::string &);
  ~MPASFile();
  int read_dim(std::string);
  std::vector<float> read_var_1d_float(std::string, int);
  std::vector<int> read_var_1d_int(std::string, int);

};
