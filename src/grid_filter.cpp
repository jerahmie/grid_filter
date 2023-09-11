/*
 * File - grid_filter.cpp
 * Filter observations against regional MPAS domain.
 */

#include <iostream>
#include <vector>
#include <memory>
#include <cmath>
#include <string>
#include <chrono>
#include <omp.h>
#include "cxxopts.hpp"
#include "mpas_file.h"
#include "obs_util.h"
#include "lam_domain_filter.h"
#include "kdtree.h"

// OpenMP Parallel LAM filtering
std::vector<int> lam_domain_filter_omp(KDTree kd2d,
                                      std::vector<point2D>::iterator obs_begin,
                                      std::vector<point2D>::iterator obs_end){
  int ithread, chunk_size;
  int data_size = obs_end - obs_begin;
  std::vector<int>::iterator obs_mask_begin;
  std::vector<int> obs_mask(data_size, 0);
  std::vector<point2D>::iterator chunk_begin, chunk_end;
  
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
    #pragma omp critical
    for (int i = 0; i < obs_mask_chunk.size(); i++) {
      *(obs_mask_begin + i) = *(obs_mask_chunk.begin() + i);
    }
  }
  return obs_mask;
}


int main(int argc, char* argv[]) {

  std::cout << "Grid Filter: " << argv[0] <<   std::endl;
  cxxopts::Options options(std::string(argv[0]), "- Filter observations points to be within MPAS regional grid.");
  options.positional_help("static-file obs_file output").show_positional_help();
  options.add_options()
    ("h,help", "Print usage")
    ("static-file", "MPAS static file (NetCDF).", cxxopts::value<std::string>())
    ("obs-file", "Observations file (HDF5).", cxxopts::value<std::string>())
    ("output", "Output mask save file (HDF5).",
       cxxopts::value<std::string>()->default_value("lam_mask.h5"));
  options.parse_positional({"static-file", "obs-file", "output"});
  auto parser = options.parse(argc, argv);

  if (parser.count("help")) {
    std::cout << options.help() << std::endl;
    return 0;
  }
  if (!parser.count("static-file")) {
    std::cout << "\nStatic File not specified. \n\n";
    std::cout << options.help() << std::endl;
    return 1; 
  }
  if (!parser.count("obs-file")) {
    std::cout << "\nObservation file not specified. \n\n";
    std::cout << options.help() << std::endl;
    return 1;
  }
  std::cout << parser["output"].as<std::string>() << '\n';
    
  auto t1 = std::chrono::high_resolution_clock::now();
  
  std::vector<int> bdy_cell_types = {6,7};
  KDTree kd2d = KDTree(parser["static-file"].as<std::string>(), bdy_cell_types);
  auto t2 = std::chrono::high_resolution_clock::now();
  auto duration_build_tree = std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1);
  
  std::string obs_file = parser["obs-file"].as<std::string>();
  std::vector<point2D> obs = read_obs_points(obs_file);

  auto t3 = std::chrono::high_resolution_clock::now();
  auto duration_read_obs = std::chrono::duration_cast<std::chrono::milliseconds>(t3-t2);
  std::vector<int> obs_mask = lam_domain_filter_omp(kd2d, obs.begin(), obs.end());
  long mask_sum = 0;
  for (auto ob : obs_mask) { mask_sum += ob; }
  auto t4 = std::chrono::high_resolution_clock::now();
  auto duration_lam_filter = std::chrono::duration_cast<std::chrono::milliseconds>(t4-t3);
  std::string outputfilename = parser["output"].as<std::string>();
  
  //std::string testgroup = "/DerivedValue";
  //std::string testdata =  "LAMDomainCheck";

  //write_mask(outputfilename, testgroup, testdata, obs_mask);
  
  std::cout << "kd2d size: " << kd2d.size() << "\n";
  std::cout << "Non-zero elements in mask: " << mask_sum  << '\n';
  std::cout << "\n=============== Time Results ================ \n";
  std::cout << "        Build tree time: " << duration_build_tree.count() << " ms\n";
  std::cout << "Read observation points: " << duration_read_obs.count() << " ms\n";
  std::cout << "             Filter obs: " << duration_lam_filter.count() << " ms\n";

  return 0;
}
