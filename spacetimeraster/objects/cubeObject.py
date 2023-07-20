from osgeo import gdal
from osgeo import osr
import numpy as np
import pandas as pd
import netCDF4 as nc
import re
from spacetimeraster.operations.time import cube_time, return_time
import xarray as xr
import psutil


class cube(object):

    def __init__(self, inputCube, fileStruc, timeObj, fileSize, names=None, inMemory = "auto"):

        # save as barracuda object
        self.cubeObj = inputCube
        self.fileStruc = fileStruc
        self.names = names
        self.timeObj = timeObj
        self.inMemory = inMemory
        self.sizes = fileSize

        if self.fileStruc == "filestovar":
            self.ind = self.names[0]
        else:
            self.ind = "value"
            self.names = None

        if str(type(self.timeObj)) == "<class 'numpy.ndarray'>":
            self.noTime = True
        else:
            self.noTime = False

    def get_GDAL_data(self):
        return self.cubeObj

    def get_file_size(self):
        if "class 'float'" in str(type(self.sizes)) or "int" in str(type(self.sizes)):
            out = self.sizes
        else:
            out = sum(self.sizes)
        return out

    def get_units(self):
        out = self.cubeObj.variables['lon'].units
        return out

    def get_band_number(self):
        out = self.cubeObj.variables["time"].shape[0]
        return out

    def get_time(self):

        if self.noTime == True:
            out = self.cubeObj.variables["time"][:]

        else:
            a = self.cubeObj.variables["time"]
            a = return_time(a)
            out = pd.to_datetime(a)

        return out

    def get_dims(self):
        y = len(self.cubeObj.variables["lat"][:])
        x = len(self.cubeObj.variables["lon"][:])
        out = [x, y]
        return out

    def get_lat(self):
        out = self.cubeObj.variables["lat"][:]
        return out

    def get_lon(self):
        out = self.cubeObj.variables["lon"][:]
        return out

    def get_UL_corner(self):
        y = self.get_lon()[0]
        x = self.get_lat()[0]
        out = [x,y]
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

    def get_var_names(self):
        out = self.names
        return out

    def get_spatial_ref(self):
        out = self.cubeObj.variables["spatial_ref"]
        return out

    def get_data_array(self, variables=None):

        if self.fileStruc == "filestotime":
            out = self.cubeObj.variables[self.ind][:]

            outMat = xr.DataArray(data=out, dims=["time", "lat", "lon"], coords=dict(
               lon=(["lon"], self.get_lon()),
               lat=(["lat"], self.get_lat()),
               time=self.get_time()))

        if self.fileStruc == "filestovar":

            outList = []
            for i in range(len(self.names)):
                outList.append(self.cubeObj.variables[self.names[i]][:])

            intDS = np.array(outList)

            out = xr.DataArray(data=intDS, dims=["variables", "time", "lat", "lon"], coords=dict(
                  variables = (["variables"], self.names),
                  lon=(["lon"], self.get_lon()),
                  lat=(["lat"], self.get_lat()),
                  time=self.get_time()))

            # allow selecting of vars
            if variables == None:
                outMat = out
            else:
                index = [self.names.index(x) for x in variables]
                outMat = out[index,:,:,:]

        if self.inMemory == False:
            outMat = outMat

        elif self.inMemory == True:
            outMat = outMat.load()

        elif self.inMemory == "auto":
            RAM = psutil.virtual_memory().total / (1024.0 ** 3)
            fileSize = self.get_file_size()

            if fileSize > (.7 * RAM):
                outMat = outMat
            else:
                outMat = outMat.load()

        return outMat

    def get_shapeval(self):

        ds = self.get_data_array()
        shapeVal = len(ds.shape)
        return shapeVal