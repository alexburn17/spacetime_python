import re
import numpy as np
from osgeo import gdal
from spacetimepy.objects.fileObject import file_object


######################################################################################################################
# DESCRIPTION: raster_trim takes a list of rasters as trims them to the greatest common dimensions
# and writes out a list of numpy arrays. The last two elements in the list are the greatest common coords
# for the upper left and lower right corners and the GDAL geo-transform output
#
# AUTHOR: P. Alexander Burnham
# 9 August 2021
# last update: 16 August 2021
#
# INPUTS:
# rastList (required): a list of raster objects typically already rescaled by the raster_align function.
#
# OUTPUT:
# A list of trimmed raster matrices with the last two elements as a vector of the greatest common coords
# for the upper left and lower right corners and the GDAL geotransform output vector
######################################################################################################################

def raster_trim(data = None, method = "intersection", ul = None, lr = None, shapeFile = None):

    outList = [] # initialize a list

    # bring in raster objects
    rastList = data.get_GDAL_data()

    # create matrix for storing corner data
    cornerArray = np.empty(shape=(len(rastList),4))

    # here is where the loop needs to be:
    for i in range(len(rastList)):

##############################################################################################################

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

            trimData = gdal.Translate('', rastList[i], projWin = [ulx, uly, lrx, lry], format='VRT')

        # append the data layers to the list
        outList.append(trimData)

        ###################################################################################################

    outObj = file_object(outList, data.get_file_size())

    return outObj
