cmake_minimum_required(VERSION 3.17)

find_package(NetCDF MODULE REQUIRED)
find_package(HDF5 MODULE REQUIRED COMPONENTS C HL)

add_executable(kdtree_bfs kdtree_bfs.cpp)
target_link_libraries(kdtree_bfs kdtree ${NETCDF_LIBRARIES})
