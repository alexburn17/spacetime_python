from osgeo import gdal
from osgeo import osr
import numpy as np
import netCDF4 as nc


class cube_meta(object):

    def __init__(self, dataList):

        # Initialize an emty storage matrix
        objMat = [None] * 4

        # main data set opened in gdal
        objMat[0] = dataList

        # get projection data
        objMat[1] = osr.SpatialReference(wkt=objMat[0].GetProjection())

        # extract geo transform from gdal object
        objMat[2]=objMat[0].GetGeoTransform()

        # set time vector
        max = objMat[0].RasterCount
        min = 0

        objMat[3] = np.arange(min, max, 1)

        # save as barracuda object
        self.cubeObj = objMat


    # returns a list of gdal or netcdf4 objects
    def get_GDAL_data(self):

        return self.cubeObj[0]

    def get_spatial_ref(self):
        out = self.cubeObj[0].GetProjection()
        return out


    # returns a list of SRS codes for each raster
    def get_epsg_code(self):

        code = self.cubeObj[1].GetAttrValue('AUTHORITY',1)
        epsg = ("EPSG:" + str(code))

        return epsg


    def get_units(self):


        unit = self.cubeObj[1].GetAttrValue('UNIT',0)

        return unit



    def get_UL_corner(self):


        v = self.cubeObj[2]
        corner = [v[i] for i in [3,0]]

        return corner



    def get_pixel_size(self):

        v = self.cubeObj[2]
        size = v[1]

        return size


    def get_band_number(self):


        bands = self.cubeObj[0].RasterCount

        return bands


    def get_time(self):

        return self.cubeObj[3]

    def get_dims(self):

        xDim = self.cubeObj[0].RasterXSize
        yDim = self.cubeObj[0].RasterYSize

        dims = tuple([xDim, yDim])

        return dims


    def get_data_range(self):

        band = (self.cubeObj[0].GetRasterBand(1))
        max = band.GetMaximum()
        min = band.GetMinimum()

        range = tuple([min, max])

        return range

    def get_nodata_value(self):

        band = (self.cubeObj[0].GetRasterBand(1))
        noDat = band.GetNoDataValue()

        return noDat


    def get_lat(self):

        # pixel size
        ysize = -self.get_pixel_size()

        # dimensions
        height = self.get_dims()[1]

        # upper left corner
        y = self.get_UL_corner()[0]

        # dimensions from 0 to max dims of dataset
        my=np.arange(start=0, stop=height)

        # get lats
        latVec = np.multiply(my, ysize) + y # latitude vector

        return latVec



    def get_lon(self):

        # pixel size
        xsize = self.get_pixel_size()

        # dimensions
        width = self.get_dims()[0]

        # upper left corner
        x = self.get_UL_corner()[1]

        # dimensions from 0 to max dims of dataset
        mx=np.arange(start=0, stop=width)

        # get lats
        longVec = np.multiply(mx, xsize) + x # latitude vector

        return longVec



