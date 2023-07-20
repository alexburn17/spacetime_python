import numpy as np
import netCDF4 as nc
import pandas as pd
import sys


class interum_cube(object):

    def __init__(self, cube = None, array = None, structure = None):

        # save as barracuda object
        self.cubeObj = cube.get_GDAL_data()
        self.array = array
        self.structure = structure

        if self.structure == True:
            self.names = np.array(array.variables)
            self.ind = self.names[0]
        if self.structure == False:
            self.ind = "value"
            self.names = None

    def get_GDAL_data(self):
        #print("WARNING! Original dataset is no longer of the same dimensions as your working cube. Please write your cube out using the write_cube() to store a .cd4 file of the correct dimensions!")
        out = self.cubeObj
        return out

    def get_units(self):
        out = self.cubeObj.variables['lon'].units
        return out

    def get_file_size(self):

        out = self.array.size

        return out

    def get_band_number(self):
        out = len(self.get_time())
        return out

    def get_time(self):

        a = self.array.time
        out = pd.to_datetime(a)
        return out

    def get_dims(self):
        y = len(self.get_lat())
        x = len(self.get_lon())
        out = [x, y]
        return out

    def get_lat(self):

        out = self.array.lat
        return out

    def get_lon(self):

        out = self.array.lon
        return out

    def get_UL_corner(self):
        y = self.get_lon()[0]
        x = self.get_lat()[0]
        out = [x,y]
        return out
    def get_spatial_ref(self):
        out = self.cubeObj.variables["spatial_ref"]
        return out
    def get_pixel_size(self):
        long = self.get_lon()
        get_pixel_size = abs(long[0]-long[1])
        return get_pixel_size

    def get_nodata_value(self):
        out = self.cubeObj.variables[self.ind].missing
        return out

    def get_epsg_code(self):
        out = self.cubeObj.variables[self.ind].code
        return out

    def get_data_array(self, variables=None):
        out = self.array
        return out

    def get_var_names(self):
        out = self.names
        return out

    def get_shapeval(self):

        ds = self.get_data_array()
        shapeVal = len(ds.shape)
        return shapeVal
