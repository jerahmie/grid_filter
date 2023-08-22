#include <iostream>
#include <vector>
#include <memory>
#include <cmath>
#include <string>
#include <chrono>
#include "cxxopts.hpp"
#include "mpas_file.h"
#include "obs_util.h"
#include "lam_domain_filter.h"
#include "kdtree.h"


int main(int argc, char* argv[]) {

  std::cout << "Grid Filter: " << argv[0] <<   std::endl;
  cxxopts::Options options(std::string(argv[0]), "- Filter observations points to be within MPAS regional grid.");
  options.positional_help("static_file obs_file output").show_positional_help();
  options.add_options()
    ("h,help", "Print usage")
    ("static_file", "MPAS static file (NetCDF).", cxxopts::value<std::string>())
    ("obs_file", "Observations file (HDF5).", cxxopts::value<std::string>())
    ("output", "Output mask save file (HDF5).",
       cxxopts::value<std::string>()->default_value("lam_mask.h5"));
  options.parse_positional({"static_file", "obs_file", "output"});
  auto parser = options.parse(argc, argv);

  //std::cout << result.count("static_file") << '\n';
  if (parser.count("help")) {
    std::cout << options.help() << std::endl;
    return 0;
  }
  if (!parser.count("static_file")) {
    std::cout << "\nStatic File not specified. \n\n";
    std::cout << options.help() << std::endl;
    return 1; 
  }
  if (!parser.count("obs_file")) {
    std::cout << "\nObservation file not specified. \n\n";
    std::cout << options.help() << std::endl;
    return 1;
  }
  std::cout << parser["output"].as<std::string>() << '\n';
    
  auto t1 = std::chrono::high_resolution_clock::now();
  //KDTree kd2d = KDTree(parser["static_file"].as<std::string>());
  
  std::vector<int> bdy_cell_types = {6,7};
  KDTree kd2d = KDTree(parser["static_file"].as<std::string>(), bdy_cell_types);
  auto t2 = std::chrono::high_resolution_clock::now();
  auto duration_build_tree = std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1);
  std::cout << "Build tree time: " << duration_build_tree.count() << '\n';
  std::cout << "kd2d size: " << kd2d.size() << '\n';
  
  std::string obs_file = parser["obs_file"].as<std::string>();
  std::vector<point2D> obs = read_obs_points(obs_file);

  auto t3 = std::chrono::high_resolution_clock::now();
  auto duration_read_obs = std::chrono::duration_cast<std::chrono::milliseconds>(t3-t2);
  std::cout << "Read observation points " << duration_read_obs.count() << '\n';
  std::vector<int> obs_mask = lam_domain_filter(kd2d, obs.begin(), obs.end());
  auto t4 = std::chrono::high_resolution_clock::now();
  auto duration_lam_filter = std::chrono::duration_cast<std::chrono::milliseconds>(t4-t3);
  std::cout << "filter obs: " << duration_lam_filter.count() << '\n';

  return 0;
}
