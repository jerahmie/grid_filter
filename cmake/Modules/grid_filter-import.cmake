# grid_filter-import.cmake

if(NOT HDF5_FOUND)
  find_dependency( HDF5 REQUIRED COMPONENTS CXX HL )
endif()
