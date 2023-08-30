cmake_minimum_required(VERSION 3.17)

find_package(NetCDF MODULE REQUIRED)

add_executable(kd2_small kd2_small.cpp)
target_link_libraries(kd2_small kdtree)

add_executable(kd2_node kd2_node.cpp)
target_link_libraries(kd2_node kdtree)

add_executable(kdtree_bfs kdtree_bfs.cpp)
target_link_libraries(kdtree_bfs kdtree ${NETCDF_LIBRARIES})
