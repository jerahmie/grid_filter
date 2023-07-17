#grid_perimeter

Python module to extract the perimeter cells of a MPAS regional grid.

Regional Grid | Regional Grid Perimeter Cells
:---------:|:-----------:
![](doc/pt_exterior1.png) | ![](doc/pt_interior2.png)

# Required Python modules
- numpy
- matplotlib
- cartopy
- cartopy.util
- geocat
- geocat-comp
- geocat-viz
- geometric_features


# Build and Test
```$ cmake -B buildtree && cmake --build buildtree```

```$ cd buildtree```

```$ ctest```

# Example

An example of using the grid_perimeter module to generate the above plots:


```$ python3 examples/plot_random_nearest.py test/python_tests/Manitowoc.static.nc```

LAM Domain Filter an observation file against a MPAS regional domain.
```$ examples/filter_obs.py static_file, obs_file, lam_mask_file ```

Example:
```$ examples/filter_obs.py conus_15km.static.nc satwind_obs_2019050100.h5 lam_domain.h5```

# Apptainer/Singularity Container
