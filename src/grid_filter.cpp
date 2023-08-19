#include <iostream>
#include <vector>
#include <memory>
#include <cmath>
#include <string>
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
       cxxopts::value<std::string>()->default_value("lam_mask.h5"))
    ;
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
    
  KDTree kd2d = KDTree(parser["static_file"].as<std::string>());
  std::string obs_file = parser["obs_file"].as<std::string>();
  std::vector<point2D> obs = read_obs_points(obs_file);
  std::vector<int> obs_mask = lam_domain_filter(kd2d, obs.begin(), obs.end());

  return 0;
}
