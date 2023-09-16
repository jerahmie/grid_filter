/*
 * file - lam_domain_filter.cpp
 * Filter observations against MPAS regional domanin.
 */

#include <vector>
#include <omp.h>
#include <cmath>
#include "lam_domain_filter.h"
#include "kdtree.h"

// OpenMP parallelized LAM domain filtering.
// Parallelized Limited Area Model Domain filtering
// a KDTree of MPAS regional domain data.
std::vector<int> lam_domain_filter_omp(KDTree &kd2d,
                                      std::vector<point2D>::iterator obs_begin,
                                      std::vector<point2D>::iterator obs_end){
  int ithread, chunk_size;
  int data_size = obs_end - obs_begin;
  std::vector<int>::iterator obs_mask_begin;
  std::vector<int> obs_mask(data_size, 0);
  std::vector<point2D>::iterator chunk_begin, chunk_end;
  // Process subdoain of observation points in OpenMP thread
#pragma omp parallel default(shared) private(ithread, chunk_begin, chunk_end, obs_mask_begin)
  {
    chunk_size = (int)ceil((double)data_size / (double)omp_get_num_threads()) -1;
    ithread = omp_get_thread_num();
    chunk_begin = obs_begin + ithread * chunk_size;
    std::vector<int>::iterator obs_mask_begin = obs_mask.begin() + ithread*chunk_size;
    if ((obs_end-chunk_begin) < chunk_size) {
      chunk_end = obs_end - 1;
    } else {
      chunk_end = chunk_begin + chunk_size;
    }

    // get filtered observation subdomain
    std::vector<int> obs_mask_chunk = lam_domain_filter(kd2d, chunk_begin, chunk_end);
    // Merge observation mask results
    #pragma omp critical
    for (int i = 0; i < obs_mask_chunk.size(); i++) {
      *(obs_mask_begin + i) = *(obs_mask_chunk.begin() + i);
    }
  }
  return obs_mask;
}

// Limited Area Model domain filter of observations against KDTree of MPAS
// regional domain points.
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

