/*
 * file - lam_domain_filter.cpp
 */

#include <vector>
#include "lam_domain_filter.h"
#include "kdtree.h"

std::vector<int> lam_domain_filter(KDTree &kd,
                                   std::vector<point2D>::iterator obs_begin,
                                   std::vector<point2D>::iterator obs_end) {
  std::vector<int> lam_mask;
  for (auto obs = obs_begin; obs < obs_end; obs++) {
    kd.find_nearest_cell_id(obs->lat, obs->lon);
   lam_mask.push_back(1); 
  }
  return lam_mask;
}

