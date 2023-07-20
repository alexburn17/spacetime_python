import numpy as np
import netCDF4 as nc

def write_netcdf(cube, dataset, fileName, organizeFiles, organizeBands, vars=None, timeObj=None):

    ds = nc.Dataset(fileName, 'w', format='NETCDF4')

    # inmtialize vars by creating dimensions
    time = ds.createDimension('time', len(timeObj)) # no time var in this case
    lat = ds.createDimension('lat', cube.get_dims()[1])
    lon = ds.createDimension('lon', cube.get_dims()[0])

    # create variables in the data set
    time = ds.createVariable('time', 'float64', ('time',))
    lats = ds.createVariable('lat', 'f4', ('lat',))
    lons = ds.createVariable('lon', 'f4', ('lon',))

    #value.units = 'My Units'
    lons.units = "degrees_east" #cube.get_units()
    lons.standard_name = "longitude"
    lons.axis = "X"

    lats.units = "degrees_north" #cube.get_units()
    lats.standard_name = "latitude"
    lats.axis = "Y"

    ds.variables['lat'][:] = cube.get_lat()
    ds.variables['lon'][:] = cube.get_lon()
    crs = ds.createVariable('spatial_ref', 'i4')
    crs.spatial_ref = cube.get_spatial_ref()


    # each file is a variable
    ############################################################################################
    numVars = len(dataset[0].shape)

    if organizeFiles == "filestovar" or organizeBands=="bandstovar":
        
        for i in range(len(vars)):

            value = ds.createVariable(vars[i], 'f4', ('time', 'lat', 'lon',))
            value.code =  cube.get_epsg_code()

            if cube.get_nodata_value() != None:
                value.missing = cube.get_nodata_value()
            else:
                value.missing = -9999


            # is it a list of arrays or a dictionary (XARRAY)
            if "<class 'dict'>" in str(type(dataset)):
                ds.variables[vars[i]][:] = np.moveaxis(dataset[vars[i]], 2, 0)
            else:
                if numVars < 3:
                    ds.variables[vars[i]][:] = dataset[i]
                else:
                    ds.variables[vars[i]][:] = np.moveaxis(dataset[i], 2, 0)


        if str(type(timeObj)) == "<class 'numpy.ndarray'>":

            ds.variables['time'][:] = timeObj

        else:

            time.units = "seconds since " + str(timeObj.to_numpy()[0])
            timeObj = timeObj.to_numpy()

            timedelta = timeObj-timeObj[0]
            seconds = np.divide(timedelta, 1e+9)
            ds.variables['time'][:] = seconds

    ############################################################################################


    # all files are times and must be stacked into one 3d cube
    ############################################################################################
    if organizeFiles == "filestotime" and organizeBands == "bandstotime":

        if 'xarray.core.dataarray.DataArray' in str(type(dataset)):
            value = ds.createVariable('value', 'f4', ('time', 'lat', 'lon',))
        else:
            value = ds.createVariable('value', 'f4', ('time', 'lat', 'lon',))
            dataset = np.moveaxis(dataset, 2, 0)

        value.code =  cube.get_epsg_code()
        if cube.get_nodata_value() != None:
            value.missing = cube.get_nodata_value()
        else:
            value.missing = -9999

        # create the main variables
        ds.variables['value'][:] = dataset

        if str(type(timeObj)) == "<class 'numpy.ndarray'>":
            ds.variables['time'][:] = timeObj
        else:
            time.units = "seconds since " + str(timeObj.to_numpy()[0])
            timeObj = timeObj.to_numpy()
            timedelta = timeObj-timeObj[0]
            seconds = np.divide(timedelta, 1e+9)

            ds.variables['time'][:] = seconds

    ############################################################################################

    return ds

    ds.close()





