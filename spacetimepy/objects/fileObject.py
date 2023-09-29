from osgeo import gdal
from osgeo import osr
import numpy as np
import netCDF4 as nc
import time


class file_object(object):

    def __init__(self, dataList, sizes):

        # Initialize an empty storage matrix
        objMat = [[0] * len(dataList) for i in range( 4 )]

        # create a list of rasters
        for i in range(len(dataList)):

            # main data set opened in gdal
            objMat[0][i] = dataList[i]

            # get projection data
            objMat[1][i] = osr.SpatialReference(wkt=objMat[0][i].GetProjection())

            # extract geo transform from gdal object
            objMat[2][i]=objMat[0][i].GetGeoTransform()

            # set time vector
            max = objMat[0][i].RasterCount
            min = 0

            objMat[3][i] = np.arange(min, max, 1)


        # save as spacetimepy object
        self.spacetimepyObject = objMat

        self.fileSize = sizes

    # returns a list of gdal or netcdf4 objects
    def get_GDAL_data(self):

        return self.spacetimepyObject[0]


    # returns a list of SRS codes for each raster
    def get_epsg_code(self):

        epsgList = []
        for i in range(len(self.spacetimepyObject[0])):

            code = self.spacetimepyObject[1][i].GetAttrValue('AUTHORITY',1)
            epsgList.append("EPSG:" + str(code))

        return epsgList



    def get_units(self):

        unitList = []
        for i in range(len(self.spacetimepyObject[0])):
            unit = self.spacetimepyObject[1][i].GetAttrValue('UNIT',0)

            unitList.append(unit)

        return unitList



    def get_UL_corner(self):

        cornerList = []
        for i in range(len(self.spacetimepyObject[0])):

            v = self.spacetimepyObject[2][i]
            corner = [v[i] for i in [3,0]]

            cornerList.append(corner)

        return cornerList




    def get_pixel_size(self):

        sizeList = []
        for i in range(len(self.spacetimepyObject[0])):

            v = self.spacetimepyObject[2][i]
            size = v[1]

            sizeList.append(size)

        return sizeList


    def get_band_number(self):

        bandList = []
        for i in range(len(self.spacetimepyObject[0])):

            bands = self.spacetimepyObject[0][i].RasterCount

            bandList.append(bands)

        return bandList


    def get_time(self):

        return self.spacetimepyObject[3]

    def get_dims(self):

        dimList = []
        for i in range(len(self.spacetimepyObject[0])):

            xDim = self.spacetimepyObject[0][i].RasterXSize
            yDim = self.spacetimepyObject[0][i].RasterYSize

            tempTup = tuple([xDim, yDim])
            dimList.append(tempTup)

        return dimList


    def get_data_range(self):

        rangeList = []
        for i in range(len(self.spacetimepyObject[0])):

            band = (self.spacetimepyObject[0][i].GetRasterBand(1))
            max = band.GetMaximum()
            min = band.GetMinimum()

            tempTup = tuple([min, max])
            rangeList.append(tempTup)

        return rangeList

    def get_nodata_value(self):

        nodatList = []

        for i in range(len(self.spacetimepyObject[0])):

            band = (self.spacetimepyObject[0][i].GetRasterBand(1))
            nodat = band.GetNoDataValue()

            nodatList.append(nodat)

        return nodatList



    def get_bands(self, min=1, max=2, rasters=None):

        outList = []

        if rasters==None:
            rasters = [0]

        for i in range(len(rasters)):
            tempMat = []
            obj = self.spacetimepyObject[0][rasters[i]]

            for j in range(max-min+1):

                band = obj.GetRasterBand(j+1).ReadAsArray()
                tempMat.append(band)

            outMat = np.stack(tempMat, axis=2)
            outList.append(outMat)

        return outList


    def get_lat(self):

        outList = []

        for i in range(len(self.spacetimepyObject[0])):

            # pixel size
            ysize = -self.get_pixel_size()[i]

            # dimensions
            height = self.get_dims()[i][1]

            # upper left corner
            y = self.get_UL_corner()[i][0]

            # dimensions from 0 to max dims of dataset
            my=np.arange(start=0, stop=height)

            # get lats
            latVec = np.multiply(my, ysize) + y # latitude vector

            outList.append(latVec)

        return outList


    def get_lon(self):

        outList = []

        for i in range(len(self.spacetimepyObject[0])):

            # pixel size
            xsize = self.get_pixel_size()[i]

            # dimensions
            width = self.get_dims()[i][0]

            # upper left corner
            x = self.get_UL_corner()[i][1]

            # dimensions from 0 to max dims of dataset
            mx=np.arange(start=0, stop=width)

            # get lats
            longVec = np.multiply(mx, xsize) + x # latitude vector

            outList.append(longVec)

        return outList


    def get_spatial_ref(self):
        outList = []

        out = self.cubeObj.variables["spatial_ref"]
        return out

    def get_file_size(self):

        return self.fileSize


    def get_data_array(self): # this is slow (SPEED IT UP)

        outList = []

        for i in range(len(self.spacetimepyObject[0])):

            tempMat = []
            obj = self.spacetimepyObject[0][i]

            for j in range(self.get_band_number()[i]):

                band = obj.GetRasterBand(j+1).ReadAsArray()
                tempMat.append(band)

            outMat = np.stack(tempMat, axis=2)
            outList.append(outMat)


        return outList



