# C++ KDTree Library

A modern C++-17 implementation of the KDTree library. This project builds *libkdtree* library that is linked into a command line utility *filter_obs*.  This is functionally equivalent to the pure Python implementation, but offers better performance.The nearest observation point search is parallelized using OpenMP for high throughput.

```bash
grid_filter/src/
|
├── CMakeLists.txt         # CMake build file
├── README.md              # This file
├── build_tree.cpp         # Helper functions to construct KDTree
├── grid_filter.cpp        # Main entry to filter_obs
├── kdtree.cpp             # KDTree class implementation
├── kdtree_node.cpp	   # KDTree node implementation
├── kdtree_util.cpp        # KDTree helper functions
├── lam_domain_filter.cpp  # Filter observation point through KDTree
├── mpas_file.cpp          # Load and process MPAS regional domain file
├── mpas_util.cpp          # Helper functions format MPAS data for KDTree build
└── obs_util.cpp           # Read and write Observation data
```
