# Grid_Filter Python Implementation

grid_filter/python/

```bash
python
├── README.md
├── __init__.py
├── grid_filter
│   ├── __init__.py
│   ├── grid_util.py      # Utility functions for processing MPAS grid values. 
│   ├── kdnode.py         # Class to representa a node element in a 2D KDTree
│   ├── kdtree.py	  # KD2D class represents an MPAS grid as a 2D KDTree.
│   ├── kdtree_util.py    # Utility and helper functions for KD-Tree building
│   ├── lam_domain_filter.py # Filter all observations, finding nearest KDTree pt.
│   ├── mpas_grid.py      # Read and store Regional MPAS grid data in a class.
│   ├── obs_data.py       # Load and save observation points from IODA hdf5 source.
│   ├── obs_mask.py       # Filter observation data using calculated mask.
│   └── regional_data.py  # Hepler functions for reading MPAS regional grid data.
└── visualization
    ├── __init__.py
    ├── kdtree_display.py # Display information about KDTree2D
    └── plot_grid.py      # Plot the MPAS grid on map projection, overplot observation points.
```
