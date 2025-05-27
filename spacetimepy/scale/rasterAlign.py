from osgeo import gdal
from spacetimepy.objects.fileObject import file_object
import numpy as np
from spacetimepy.input.readData import read_data
import re

######################################################################################################################
# DESCRIPTION: This function called raster_align takes a list of raster names, loads the rasters
# into memory and ensures they have the same aligned structure with the correct SRS codes and consitant resolutions
#
# AUTHOR: P. Alexander Burnham
# 5 August 2021
# last update: 27 May 2025
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
def raster_align(data=None, resolution="min", SRS=4326, noneVal=None, algorithm="near", template = None, method = "intersection", ul = None, lr = None, shapeFile = None):

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



# Trimming Data code
##############################################################################################################

    rastList = data.get_GDAL_data()
    cornerArray = np.empty(shape=(len(rastList),4))

    # here is where the loop needs to be:
    for i in range(len(rastList)):

        # get meta data for each raster
        meta = gdal.Info(rastList[i])

        # use regex to extract upper and lower right corners
        Uleft = re.search(r'Upper Left  \(([^)]+)', meta).group(1)
        Lright = re.search(r'Lower Right \(([^)]+)', meta).group(1)

        # create full string
        corners = Uleft + ',' + Lright

        # numeric list of corners (upper left [0-1] and lower right [2-3])
        cornersList = corners.split(',')
        cornersList = [ float(x) for x in cornersList ]

        # add corners to an array
        cornerArray[i,:] = cornersList

########################################################################################################################

    # find greatest common dimensions to crop rasters to:
    # highest x, lowest y (upper left corner): lowest x, highest y (lower right corner)
    if method == "intersection":
        cornersCommon = [np.max(cornerArray[:,0]), np.min(cornerArray[:,1]), np.min(cornerArray[:,2]), np.max(cornerArray[:,3])]

    if method == "union":
        cornersCommon = [np.min(cornerArray[:,0]), np.max(cornerArray[:,1]), np.max(cornerArray[:,2]), np.min(cornerArray[:,3])]

    if method == "corners":
        cornersCommon = ul + lr

    # loop to find common bounding box
    for i in range(len(rastList)):

        # trim the matrix
        if shapeFile != None and method == "shape":

            trimData = gdal.Warp('', rastList[i], cutlineDSName = shapeFile, cropToCutline=True, format='VRT')


        else:

            # common corners
            ulx=cornersCommon[0]
            uly=cornersCommon[1]
            lrx=cornersCommon[2]
            lry=cornersCommon[3]



    def convert_bounds(ulx, uly, lrx, lry):
        xmin = min(ulx, lrx)
        xmax = max(ulx, lrx)
        ymin = min(uly, lry)
        ymax = max(uly, lry)
        return [xmin, ymin, xmax, ymax]

    crop_bounds = convert_bounds(ulx, uly, lrx, lry)

    # do transformation and alignment
    for i in range(objSize):
        dataMat[1][i] = gdal.Warp('', dataMat[0][i], targetAlignedPixels=True, dstSRS=SRS_code, format='VRT',
        xRes=resolution, yRes=-resolution, dstNodata=noneVal, resampleAlg=algorithm, outputBounds=crop_bounds, cropToCutline=True)

    # make a cube object
    outObj = file_object(dataMat[1], data.get_file_size())



    return outObj
######################################################################################################################
# END FUNCTION
######################################################################################################################