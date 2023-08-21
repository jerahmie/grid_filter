/*
 * file - obs_util.h
 */

#pragma once
#include <vector>
#include <string>
#include "kdtree_util.h"

std::vector<float> read_h5data(std::string&, std::string, std::string);
std::vector<point2D> read_obs_points(std::string&);
