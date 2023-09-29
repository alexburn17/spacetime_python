import numpy as np
import netCDF4 as nc
from spacetimepy.objects.interumCube import interum_cube
import xarray as xr
from spacetimepy.operations.makeCube import make_cube
from datetime import date
from random import randint


def cube_smasher(function = None, eq = None, parentCube = None, fileName = None, **kwarg):

    # is there a parent cube and what is the file structure?
    if parentCube != None:
        if type(parentCube.get_var_names()) == type(None):
            filestovar = False
        else:
            filestovar = True

    # loop through input dict to extract raster data for operations
    for key in kwarg:
        if "list" in str(type(kwarg[key])):
            for i in range(len(kwarg[key])):
                if "cube" in str(type(kwarg[key][i])):
                    kwarg[key][i] = kwarg[key][i].get_data_array()
        else:
            if "cube" in str(type(kwarg[key])):
                kwarg[key] = kwarg[key].get_data_array().to_numpy()

    # do operations as below
    if function == None:
        y = eval(eq, kwarg)

    if eq == None:
        y = function(**kwarg)

    if parentCube == None:
        out = y

    else:
        time = parentCube.get_time()
        lon = parentCube.get_lon()
        lat = parentCube.get_lat()
        variables = parentCube.get_var_names()

        c = np.where(parentCube.get_data_array() == parentCube.get_nodata_value(), parentCube.get_nodata_value(), y) #, parentCube.get_data_array(), y

        dims = len(c.shape) # how many dimensions in array


        if dims == 3:

            y = xr.DataArray(data=c, dims=["time", "lat", "lon"], coords=dict(
                lat=(["lat"], lat),
                lon=(["lon"], lon),
                time=time))

        if dims > 3:

            y = xr.DataArray(data=c, dims=["variables", "time", "lat", "lon"], coords=dict(
                variables = (["variables"], variables),
                lon=(["lon"], lon),
                lat=(["lat"], lat),
                time=time))

        int = interum_cube(cube = parentCube, array = y, structure = filestovar)

        if fileName == None:
            # file name
            now = date.today()
            num = str(randint(100, 999))
            file = "cube_smasher_" + str(now) + "_" + num + ".nc4"
        else:
            file = fileName

        out = make_cube(data = int, fileName = file)

    return out








