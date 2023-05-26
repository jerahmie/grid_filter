"""
Test if graphics packages are working as expected.
"""
import os
import unittest
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geocat.viz as gv

class TestGraphicsPackages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maponly_file = os.path.join(os.getcwd(), 'maponly.png')
        if os.path.exists(cls.maponly_file):
            os.remove(cls.maponly_file)

    def setUp(self):
        pass

    def test_install_setup(self):
        """
        Test the installation and unittest setup.  Should always pass.
        """
        self.assertTrue(True)

    def test_gencart(self):
        """
        Generate a map with only land features and save to file.
        See: shorturl.at/jrwFN
        """
        # generate axes using Cartopy
        ax = plt.axes(projection=ccrs.PlateCarree())

        # draw land
        ax.add_feature(cfeature.LAND, color='silver')

        # add axes tick values
        gv.set_axes_limits_and_ticks(ax,
                                     xticks=np.linspace(-180, 180, 13),
                                     yticks=np.linspace(-90, 90, 7))

        # add major and minor ticks
        gv.add_major_minor_ticks(ax)

        # save plot
        print(self.maponly_file)
        plt.savefig(self.maponly_file)
        self.assertTrue(os.path.exists(self.maponly_file))

    def test_gensat(self):
        """
        Test generating a global projection.
        see: shorturl.at/mpsHN
        """
        # create figure and set size
        fig = plt.figure(figsize=(8, 8))

        # set global axes with orthographic projection
        proj = ccrs.Orthographic(central_longitude=270, central_latitude=45)
        ax = plt.axes(projection=proj)
        ax.set_global()

        ax.add_feature(cfeature.LAND, facecolor='lightgray')
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
        ax.add_feature(cfeature.OCEAN, facecolor='lightcyan')
        ax.add_feature(cfeature.BORDERS, linewidth=0.5)
        ax.add_feature(cfeature.LAKES,
                       facecolor='blue',
                       edgecolor='black',
                       linewidth=0.5)
        ax.add_feature(cfeature.STATES,
                       facecolor='darkgray',
                       edgecolor='black',
                       linewidth=0.3)
        ax.add_feature(cfeature.RIVERS,
                       facecolor='blue',
                       edgecolor='black',
                       linewidth=0.1)
        # make tight layout
        plt.tight_layout()
        plt.savefig('satellite_map.png')

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()
