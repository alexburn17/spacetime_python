from osgeo import gdal
from spacetimepy.objects.fileObject import file_object
import numpy as np
from spacetimepy.input.readData import read_data


######################################################################################################################
# DESCRIPTION: This function called raster_align takes a list of raster names, loads the rasters
# into memory and ensures they have the same aligned structure with the correct SRS codes and consitant resolutions
#
# AUTHOR: P. Alexander Burnham
# 5 August 2021
#
# INPUTS:
# rastNames (required): a list or array of file names including the required path if in another directory.
# resolution: the pixel dimensions to be used for all rasters. Defaults to the largest common pixel size
# SRS: this is the SRS code that sets the units and geospatial scale. Defaults to EPSG:3857 like google maps
# noneVal: the value to be used for pixels in the raster that contain no value. Defaults to -9999
#
# OUTPUT:
# It outputs a list of rescaled and geospatialy aligned rasters
######################################################################################################################
def raster_align(data=None, resolution="min", SRS=4326, noneVal=None, algorithm="near", template = None):

    if SRS == None:
        SRS_code = data.get_epsg_code()[0]
    else:
        # define the espg code as a character for GDAL
        SRS_code = "EPSG:" + str(SRS)
    if noneVal == None:
        noneVal = data.get_nodata_value()[0]

    objSize = len(data.get_epsg_code()) # time dimension for list

    # initialize a mat to store files in during the loop and one to store the modification
    dataMat = [[0] * objSize for i in range(2)]

    # list for pixel sizes after rescaled
    reso = []

    # create a list of rasters in first column
    for i in range(objSize):
        dataMat[0][i] = data.get_GDAL_data()[i]

        # get list of resolutions
        ps = gdal.Warp('', dataMat[0][i], dstSRS=SRS_code, format='VRT')
        reso.append(ps.GetGeoTransform()[1])


    # pick the resolution
    if resolution == "max":
        resolution = np.min(reso)
    if resolution == "min":
        resolution = np.max(reso)
    else:
        resolution = resolution

    # do transformation and alignment
    for i in range(objSize):
        dataMat[1][i] = gdal.Warp('', dataMat[0][i], targetAlignedPixels=True, dstSRS=SRS_code, format='VRT',
        xRes=resolution, yRes=-resolution, dstNodata=noneVal, resampleAlg=algorithm)

    #print((dataMat[1][0]).GetRasterBand(1).ReadAsArray())
    # make a cube object
    outObj = file_object(dataMat[1], data.get_file_size())



    return outObj
######################################################################################################################
# END FUNCTION
######################################################################################################################