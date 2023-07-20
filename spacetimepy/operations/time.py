import pandas as pd
import netCDF4 as nc
import numpy as np
from spacetimepy.objects.interumCube import interum_cube
import xarray as xr


########################################################################################################################
def cube_time(start=None, length=None, scale=None, skips = 1):

    if scale == "year":
        skips = str(skips) + "Y"

    if scale == "month":
        skips = str(skips) + "M"

    if scale == "day":
        skips = str(skips) + "D"

    dates = pd.date_range(start, periods=length, freq=skips).tolist()

    out = pd.to_datetime(dates)


    return out
########################################################################################################################



########################################################################################################################
def return_time(timeObject):

    timeList = nc.num2date(timeObject, timeObject.units)
    a = [np.datetime64(x) for x in timeList]
    np64 = pd.to_datetime(a)

    return np64

########################################################################################################################





########################################################################################################################
def select_time(cube, range="entire", scale = None, element=None):

    ds  = cube.get_data_array()

    if range == "entire":

        # select the element
        if scale == "day":
            x = ds.where(ds['time.day'] == element, drop=True)
        if scale == "month":
            x = ds.where(ds['time.month'] == element, drop=True)
        if scale == "year":
            x = ds.where(ds['time.year'] == element, drop=True)

    else:

        x=ds.sel(time=slice(range[0], range[1]))

        if element != None:
            # select the element
            if scale == "day":
                x = x.where(x['time.day'] == element, drop=True)
            if scale == "month":
                x = x.where(x['time.month'] == element, drop=True)
            if scale == "year":
                x = x.where(x['time.year'] == element, drop=True)

    if len(ds.shape) >= 4:
        filestovar = True
    else:
        filestovar = False

    out = interum_cube(cube = cube, array = x, structure = filestovar)

    return out



########################################################################################################################





########################################################################################################################
def scale_time(cube, scale, method):

    format = cube.get_time()

    if "DatetimeIndex" in str(type(format)):

        dictArray = cube.get_data_array()
        ds = dictArray.where(dictArray != cube.get_nodata_value())

        if scale == "month" and method == "mean":
            x = ds.resample(time="1M").mean(skipna=False)
        if scale == "year" and method == "mean":
            x = ds.resample(time="1Y").mean(skipna=False)
        if scale == "day" and method == "mean":
            x = ds.resample(time="1D").mean(skipna=False)
        if scale == "month" and method == "max":
            x = ds.resample(time="1M").max(skipna=False)
        if scale == "year" and method == "max":
            x = ds.resample(time="1Y").max(skipna=False)
        if scale == "day" and method == "max":
            x = ds.resample(time="1D").max(skipna=False)

        if len(ds.shape) >= 4:
            filestovar = True
        else:
            filestovar = False

        ret = interum_cube(cube = cube, array = x, structure = filestovar)

    else:
         print("Error! Time vector is not a date object. Add a date object to your cube and try again.")
         quit() # exit program and display message when no file names provided
    return ret

####

def expand_time(cube, target_time, starting_scale = "month", target_scale = "day"):

    startTime = cube.get_time()
    array = cube.get_data_array()
    numVars = len(array.shape)

    if starting_scale == "month" and target_scale == "day":

        # number of days in each month
        unique, counts = np.unique(target_time.month, return_counts=True)

        # expand input cube by counts of each month
        outList = []
        for t in range(len(counts)):
            outList.append(np.tile(array[t,:,:], (counts[t], 1, 1)))

        # concatenate the list of arrays into one array
        out = np.concatenate(outList, axis = 0)

        # make into an xarray variable
        if numVars == 3:

            outMat = xr.DataArray(data=out, dims=["time", "lat", "lon"], coords=dict(
               lon=(["lon"], cube.get_lon()),
               lat=(["lat"], cube.get_lat()),
               time=target_time))

        if numVars > 3:

            outList = []
            for i in range(len(self.names)):
                outList.append(self.cubeObj.variables[self.names[i]][:])

            intDS = np.array(outList)

            out = xr.DataArray(data=intDS, dims=["variables", "time", "lat", "lon"], coords=dict(
                  variables = (["variables"], self.names),
                  lon=(["lon"], self.get_lon()),
                  lat=(["lat"], self.get_lat()),
                  time=self.get_time()))


        ret = interum_cube(cube = cube, array = outMat)
        return(ret)