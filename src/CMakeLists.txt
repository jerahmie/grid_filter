cmake_minimum_required(VERSION 3.17)

# Lightweight command line parser.
include(FetchContent)
FetchContent_Declare(
  cxxopts
  GIT_REPOSITORY https://github.com/jarro2783/cxxopts.git
  GIT_TAG       v3.1.1
  GIT_SHALLOW   TRUE
  )
set(CXXOPTS_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
set(CXXOPTS_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(CXXOPTS_ENABLE_INSTALL CACHE BOOL "" FORCE)
set(CXXOPTS_ENABLE_WARNINGS OFF CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(cxxopts)

message(STATUS "${CMAKE_MODULE_DIR}")

find_package(NetCDF MODULE REQUIRED)
find_package(HDF5 COMPONENTS C HL)
find_package(OpenMP REQUIRED)

add_library(kdtree STATIC kdtree_node.cpp build_tree.cpp
                          kdtree_util.cpp mpas_util.cpp
                          obs_util.cpp mpas_file.cpp
                          lam_domain_filter.cpp kdtree.cpp)

target_include_directories(kdtree PUBLIC .)

add_executable(filter_obs grid_filter.cpp)

include_directories(${HDF5_INCLUDE_DIRS})

target_link_libraries(filter_obs
    cxxopts
    kdtree
    ${NETCDF_LIBRARIES} 
    ${HDF5_LIBRARIES}
    OpenMP::OpenMP_CXX)

set_property(TARGET filter_obs PROPERTY CXX_STANDARD 17)
