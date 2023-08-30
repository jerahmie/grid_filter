/*
 * file - obs_util.h
 * Utilities to read and preprocess observation data.
 */

#pragma once
#include <vector>
#include <string>
#include <typeinfo>
#include <hdf5.h>
#include "kdtree_util.h"

std::vector<float> read_h5data(std::string&, std::string, std::string);

int write_mask(std::string &, std::string &,
                  std::string &,  std::vector<int> &);

std::vector<point2D> read_obs_points(std::string&);
