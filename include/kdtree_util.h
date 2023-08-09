#pragma once

#include <memory>
#include <vector>
#include <tuple>
#include "kdtree_node.h"

bool compare_lat(nodeData, nodeData);

bool compare_lon(nodeData, nodeData);

std::tuple<nodeData, int> median_point_id(const std::vector<nodeData>&);

