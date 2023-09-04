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
    if ((obs->lat < kd.lat_min) || (obs->lat > kd.lat_max) ||
        (obs->lon < kd.lon_min) || (obs->lon > kd.lon_max)) {
    // fast prefilter
     lam_mask.push_back(0);
    } else {
      // kd-tree search
      int bdy_type = kd.find_nearest_cell_type(obs->lat, obs->lon);
      if (bdy_type == BDYCELL) {
        lam_mask.push_back(0);
      } else {
        lam_mask.push_back(1);
      }
    }
  }
  return lam_mask;
}

