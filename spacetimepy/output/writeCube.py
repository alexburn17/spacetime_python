import netCDF4 as nc
import numpy as np
from osgeo import gdal

######################################################################################################################
# DESCRIPTION: write_cube writes out a .nc file from the input of the raster_trim function and
# creates a netCDF4 dataset as a side effect
#
# AUTHOR: P. Alexander Burnham
# 11 August 2021
#
# INPUTS:
# rastList (required): a list of trimmed raster arrays from raster_trim
# yCoords: a vector for all of the y coordinates (lats)
# xCoords: a vector for all of the x coordinates (lons)
# fileName: a character string for the path and file name of the .nc file
#
# OUTPUT:
# It outputs a netCDF4 dataset and writes a .nc file to disk
######################################################################################################################

def write_cube(rastList=None, yCoords=None, xCoords=None, fileName=None, timePoints=None):

    if rastList is None:
                print("Error: No raster list provided! Please pass write_cube a list of rasters processed by raster_trim.")
                quit() # exit program and display message when no file names provided

    data = rastList[: len(rastList) ]

    ds = nc.Dataset(fileName, 'w', format='NETCDF4')

    # inmtialize vars by creating dimensions (long=X)
    time = ds.createDimension('time', timePoints) # no time var in this case
    lat = ds.createDimension('lat', len(yCoords))
    lon = ds.createDimension('lon', len(xCoords))

    # create variables in the data set
    times = ds.createVariable('time', 'f4', ('time',))
    lats = ds.createVariable('lat', 'f4', ('lat',))
    lons = ds.createVariable('lon', 'f4', ('lon',))
    value = ds.createVariable('value', 'f4', ('time', 'lat', 'lon',))
    value.units = 'My Units'


    # create the main variables
    ds.variables['value'][0:len(data)] = data
    ds.variables['lat'][:] = yCoords #add lat vals
    ds.variables['lon'][:] = xCoords # add long vals
    ds.variables['time'][:] = np.arange(timePoints)

    return ds

    ds.close() # close the dataset out in memory

# plot seasons spring-spring to spring
# control charts
# difference chart
# what do you want to convey with