# grid_perimeter

Python module to extract the perimeter cells of a MPAS regional grid.

Exterior Point | Interior Point
:---------:|:-----------:
![](doc/pt_exterior1.png) | ![](doc/pt_interior2.png)



# Build and Test
```
$ git clone git@github.com:jerahmie/grid_filter.git
$ cd grid_filter
$ mkdir buildtree && cd buildtree
$ cmake .. && make
```
The tests can be run with ctest.

```$ ctest```

To enble Python unittests, set `PYTHON_UNITTESTS=1`:
```$ cmake -DPYTHON_UNITTESTS=1 .. && ctest ```

# Python Components
## Required Python modules
- numpy
- matplotlib
- cartopy
- cartopy.util
- geocat
- geocat-comp
- geocat-viz
- geometric_features

The python grid_filter module is installed locally with pip using the '-e' flag (editable).


```$ pip install -e /path/to/grid_filter```

It is recommended to use a virtual environment with the above packages installed.  

## Notes for Building on Cheyenne
The following configurations have been tested for the following compiler sets and configurations:
### GNU

### Intel

### Python


# Example

An example of using the grid_perimeter module to generate the above plots:


```$ python3 examples/plot_random_nearest.py test/python_tests/Manitowoc.static.nc```

LAM Domain Filter an observation file against a MPAS regional domain.

```$ filter_obs <static_file> <obs_file lam_mask_file> <output_file>```

Example:

```$ filter_obs conus_15km.static.nc satwind_obs_2019050100.h5 lam_domain.h5```

Plot Filtered Observations:

```$ examples/plot_obs.py satwind_obs_2019050100.h5 --mask-file lam_domain.h5 --output lam_domain.png```

No Filter |  Filter
:---------:|:-----------:
![](doc/plot_obs_nomask.png) | ![](doc/plot_obs_masked.png)
