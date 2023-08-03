cmake_minimum_required(VERSION 3.17)
add_subdirectory(grid_filter) 

find_package(HDF5 COMPONENTS CXX HL)
#add_library(kdtree STATIC grid_filter/grid_filter.cpp)

include_directories(${HDF5_INCLUDE_DIRS})
add_executable(myh5dump myh5dump.cpp)
target_link_libraries(myh5dump ${HDF5_CXX_LIBRARIES})

add_library(kdtree STATIC kdtree_node.cpp kdtree_util.cpp kdtree.cpp)

target_include_directories(kdtree PUBLIC .)
