/*
 * file - kdtree_util.h
 *
 * Helper functions for KDTree filtering.
 */


#pragma once

#include <memory>
#include <vector>
#include <tuple>
#include "kdtree_node.h"

struct point2D { double lat; double lon; };

bool compare_lat(nodeData, nodeData);

bool compare_lon(nodeData, nodeData);

std::tuple<nodeData, int> median_point_id(const std::vector<nodeData>&);

double euclidean_1d_distance_sq(point2D, point2D, int);

double euclidean_2d_distance_sq(point2D, point2D);

