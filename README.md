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


# Apptainer/Singularity Container

# Example

An example of using the grid_perimeter module to generate the above plots:


```$ python3 examples/plot_random_nearest.py test/python_tests/Manitowoc.static.nc```


```ctest --build-and-test . buildtree --build-generator Unix Makefiles --test-command ctesti```
