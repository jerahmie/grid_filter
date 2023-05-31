cmake_minimum_required(VERSION 3.17)
add_subdirectory(grid_filter) 

#add_library(kdtree STATIC grid_filter/grid_filter.cpp)
add_library(kdtree STATIC kdtree_node.cpp kdtree.cpp)
target_include_directories(kdtree PUBLIC .)

