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
```$ cmake -DPYTHON_UNITTESTS=1 .. && make -j8 && ctest ```

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
```Currently Loaded Modules:
  1) gnu/10.1.0   2) netcdf/4.8.1   3) git/2.33.1   4) mpt/2.25   5) ncarcompilers/0.5.0   6) ncarenv/1.3   7) cmake/3.18.2```

### Intel

```Currently Loaded Modules:
  1) intel/19.1.1   2) netcdf/4.8.1   3) ncarenv/1.3   4) ncarcompilers/0.5.0   5) mpt/2.25   6) cmake/3.18.2```

### Python
The module was tested using an Anaconda virtual environment:
```$ conda create --name myenv
$ conda activate myenv
(myenv) $ conda install -c ncar geocat-comp geocat-viz
(myenv) $ conda install netcdf4 h5py
(myenv) $ pip install -e /path/to/grid_filter
```

# Example

LAM Domain Filter an observation file against a MPAS regional domain.

```$ examples/filter_obs.py <static_file> <obs_file lam_mask_file> <output_file>```

Example:

```$ examples/filter_obs.py conus_15km.static.nc satwind_obs_2019050100.h5 lam_domain.h5```

Plot Filtered Observations:

```$ examples/plot_obs.py satwind_obs_2019050100.h5 --output lam_domain.png```

No Filter |  Filter
:---------:|:-----------:
![](doc/plot_obs_nomask.png) | ![](doc/plot_obs_masked.png)

An example of using the grid_perimeter module to generate the above plots:

```$ python3 examples/plot_random_nearest.py test/python_tests/Manitowoc.static.nc```
