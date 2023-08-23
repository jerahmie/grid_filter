/*
 * file - lam_domain_filter.h
 *
 */
#pragma once

#include <vector>
#include "kdtree.h"

#define BDYCELL 7

std::vector<int> lam_domain_filter(KDTree &,
                                   std::vector<point2D>::iterator,
                                   std::vector<point2D>::iterator);

