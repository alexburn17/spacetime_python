
![spacetimepy logo](barraLogo.jpg)


-----------------

# spacetimepy Documentation

The main objective of the spacetimepy python is to make tasks like loading, rescaling, merging, and conducting mathmatical operations on spatiotemporal (or other D-dimensional data sets) easier for the user by providing a set of concise yet powerful functions. spacetimepy opperations utilize a cube-like structure for all data sets that makes storing and manipulating large D-dimensional datasets more efficient. For scientists working with spatiotemporal data (such as climate or weather data sets) spacetimepy is an ideal platform that allows the user to focus on the science rather than the coding. spacetimepy is in the beta stage (version number = 0.0.1) and additional functionality will be added on a regular basis. The current functionality of spacetimepy is below:


## spacetimepy Objects:


###`fileObj.methods():`
**Description:**  File objects are the output of the `read_data()` fucntion. They are essentially a list object of all the raster files that were read in. All methods of a file object result in a list of outputs (one for each raster in the object). File objects can contain rasters of various scales, time lengths, and sizes. The functions `raster_scale()` and `raster_align()` may be used on file objects to return a file object that contains aligned and trimmed rasters.		
**General output of methods:** A list of output objects of the length of the list of raster objects loaded by `read_data()`.		

* `get_GDAL_data()` - Extracts GDAL data object			
* `get_epsg_code()` - extracts spatial reference system EPSG code				
* `get_units()`	- extracts units of spatial grid	
* `get_UL_corner()`	- Extracts lat and long coords of the upper left corner	
* `get_band_number()` - Extracts the number of bands		
* `change_time(start, stop, interval)` - Changes the time values associated with bands
	* start = (int or list)	of starting time/date/year 
	* start = (int or list)	of ending time/date/year
	* interval = (numeric) interval between times
* `get_time()` - extracts time values (default = 0-N)		
* `get_dims()` - Extracts raster x and y dimensions				
* `get_nodata_value()` - returns no data values		
* `get_data_array()` - get full raster data set as numpy array		
* `get_bands(min=1, max=2, rasters = [0])` get subset of raster data as numpy array
	* min = (int >= 1) first raster band to extract
	* max = (int <= number of bands) last raster band to extract
	* rasters = (list) list of rasters (0-number of rasters) to pull from	 
* `get_lat()` - get latitude values		
* `get_lon()` - get longitude values		

```python
# extract list of raster data cubes from file object
dataArray = ds.get_data_array()

```




###`cubeObj.methods():`
**Description:**  Cube objects are the main operational unit in the spacetimepy package. Cube objects are cleaned, aligned D-dimensioal cube-liek datasets that minamally contain a data cube, a time dimension, and latitude and longitude (y, x) dimensions. They are the output of the `make_cube()` function. Cube objects may be passed to functions like `cube_smasher()`, `cube_plotter()` etc. to be operated on mathematically or functionally and visualized.
**General output of methods:** The associated value for the cube object as specified by the method.		

* `get_GDAL_data()` - Extracts original data object			
* `get_epsg_code()` - extracts spatial reference system EPSG code				
* `get_units()`	- extracts units of spatial grid	
* `get_UL_corner()`	- Extracts lat and long coords of the upper left corner	
* `get_band_number()` - Extracts the number of bands		
* `get_time()` - extracts time values
			
* `get_dims()` - Extracts raster x and y dimensions				
* `get_nodata_value()` - returns no data values		
* `get_data_array(variables)` - return a full D-dimensional raster data set as an xarray dataArray. 
	* variables = selects variables to return if cube was created with the "filestovar" option. Takes a list of character string variable names. 				 
* `get_lat()` - get latitude values		
* `get_lon()` - get longitude values

*  `get_var_names()` - get the variable names of the cube		

```python
# extract latitude dimension from cube object
lat = ds.get_lat()

```





## spacetimepy Functions:
**Description:** spacetimepy functions conduct scaling, plotting, writing and other tasks on spacetimepy objects.


### `read_data(data=None)`
* **Functionality:** Reads in one or multiple raster data files and prepares them for data extraction and/or use with other spacetimepy functions.
* **Input:** data = list object containing file names of rasters 
* **Output:** file object
* **Additional Arguments:** None
* Example function call:

```python
# read in data set from raster files
ds = read_data(data=rasterList)

```

### `make_cube(data = None, fileName = None, organizeFiles="filestotime", organizeBands="bandstotime", varNames=None, timeObj=None)`
* **Functionality:** Writes input objects as a cd4 file to disk and returns a virtualized cube object. **Note: for larger datasets, the writing of the cube to disk may take a few minutes**
* **Input:** data = file object or cube object
* **Output:** cube object
* **Additional Arguments:**
	* **outFile** = (char) name of outfile with preferred supported extension. 
	* **organizeFiles** = how files are organized in cube (chr).
		* "filestotime" stacks all files along the time dimension
		* "filestovar" creates a higher dimensional cube where each cube is a different variable and time are bands within each raster. 	* **organizeBands** = how bands are treated when assembling the cube (chr).
		* "bandstotime" = bands are a time dimension
		* "bandstovar" = bands are variables
	* **varNames** = a list of character strings that are the variable names for each file if the "filestovar" option is selected 
	* **timeObj** = A time object created by `cube_time()` of the desired time length. If not specified, time defaults to integers 0 to length of cube stack.
* Example function call:

```python
make_cube(data = fileObject, fileName = "test.nc4", organizeFiles = "filestovar", varNames = ["SpA","SpB"], timeObj = years)
``` 



### `raster_align(data=None, resolution=None, SRS=None, noneVal=None)`
* **Functionality:** Sets input object to have same spatial reference system and resolution and alignment.
* **Input:** data = file object as outputted by `read_data()` 
* **Output:** aligned and rescaled cube or file objects
* **Additional Arguments:** 
	* **resolution** = (numeric) intended grid size of the outputted data set in either degrees or meters depending on the spatial reference system in use.
		* **Default value:** largest resolution in data set in input spacetimepy object
	* **SRS** = (int) intended 4-digit spatial reference system code that all data sets in the outputted spacetimepy object will use.
		* **Default value:** EPSG of first data set in input object
	* **noneVal** = (numeric) no data value to be used by all datasets in the outputted spacetimepy object.
		* **Default value:** no data value of first data set in input spacetimepy object
* Example function call:

```python
dsAligned = raster_align(data=fileObj, resolution=.08, SRS=4326, noneVal=-9999)
``` 


### `raster_trim(data=None)`
* **Functionality:** Trims datasets in the input object to have the same bounding box (i.e. spatial dimensionality).
* **Input:** data = aligned file as outputted by `data_align()` 
* **Output:** file or cube object trimmed to greatest common bounding box
* **Additional Arguments:** = None
* Example function call:

```python
dsTrimmed = raster_trim(data=cubeObj)
``` 


### `cube_time(start, length, scale)`
* **Functionality:** Creates a time object that is a vector of a desired lenghth of dates or times.
* **Inputs:** 
	* **start** = starting date (chr)
	* **length** = length of desired time vector (int)
	* **scale** = resolution of time vector (chr) options are: "year", "month", "day", "hour", "minute" or "second"
* **Output:** file or cube object trimmed to greatest common bounding box
* **Additional Arguments:** = None
* Example function call:

```python
yearObj = cube_time(start="2000", length=202, scale = "year")
``` 

### `scale_time(cube, scale, method)`
* **Functionality:** Summarizes a cube by some method at a temporal scale of the user's choosing.
* **Inputs:** 
	* **cube** = a spacetimepy cube object
	* **scale** = the temporal scale the cube is to be summarized upon ("day", "month", "year")
	* **method** = the summary method options are: "mean", "max", "min", "median"
* **Output:** a new cube object with rescaled time
* Example function call:

```python
scale_time(cube=ds, scale="month", method="max")
``` 

### `select_time(cube, range="entire", scale = None, element=None)`
* **Functionality:** Select a range and or specific temporal element to extract form a data cube such as specific days, months or years.
* **Inputs:** 
	* **cube** = a spacetimepy cube object
	* **range** = (pair of character strings as a list or tuple) the range to be selected. Either a list of the first and last date to be extracted or the default "entire" argument, which extracts all time points.
	* **scale** = the temporal scale of the elements to be extracted ("day", "month", "year")
	* **element** = (int) a numeric year, month or day value
	* **Output:** a new subsetted cube object
* Example function call:

```python
select_time(cube=cubeObj, range=['2000-02-29', '2000-04-30'], scale = "month", element=4)
``` 



### `cube_smasher(function = None, eq = None, parentCube = None, **kwarg))`
* **Functionality:** Takes cube objects, arrays or scalar values, and conducts mathematical and functional operations on them as specified.
* **Input:** data = cube objects, numpy arrays or scalar values.
* **Output:** returns new cube object after opperations are completed
* **Additional Arguments:**
	* **function** = name of user specified function to pass to `cube_smasher()`
	* **eq** = (string) mathmatical equation to perform on data
	* **parentCube** = (cube object) The starting cube that the output cube should use as a guide for reconstruction (defaults to first detected cube if multiple are passed)
	* **kwarg** = additional params to pass for user specified function if not using `eq` 
* Example function call:

```python
# mathmatical operations on two tif files
outputCube = cube_smasher(eq = "a + b ** c", a=cube1, b=cube2, c = 5, parentCube = cube1)


# conduct mathmatical operation on two cube objects
outputCube = cube_smasher(eq = "a + b", a=obj1, b=obj2, parentCube = obj1)
``` 

### `cube_to_dataframe(cube)`
* **Functionality:** Takes a cube object and returns a pandas dataframe that can be used with external plotting functions.
* **Input:** cube = a cube object of any dimension 
* **Output:** Pandas dataframe with all index variables as columns.
* **Additional Arguments:** = None
* Example function call:

```python
# convert a cube into a dataframe
df = cube_to_dataframe(cube=cubeObject)
```

### `plot_cube(cube, type="space", variable = None, summary="mean", showPlot = True)`
* **Functionality:** Plots data sets as either a heatmap playable over the time dimension if applicable, or a time series plot of a user selected summary statistic.
* **Input:** data = cube object
* **Output:** data frame used to make the plot with the figure shown as a side effect
* **Additional Arguments:**
	* **variable** = (char) character string of the variable to plot spatialy if their are more than one. If not specified default is the first variable.
	* **type** = (char) select between spatial ("space") or temporal ("time_series").
	* **dataSet** = (int) selects data set within object to plot 
	* **summary** = (char) selects intended summary statistic for temporal plot. ("mean", "max", "min", "median")
	* **showPlot** = (boolean) turn off plotting and return only the plotting dataframe.
* Example function call:

```python
df = plot_cube(cube=x, variable="B", type="space", summary = "max", showPlot = True)
``` 

### `load_cube(file)`
* **Functionality:** Takes a .nc4 file as outputted by the spacetimepy `make_cube()` function and loads it back in as a cube object.
* **Input:** file = a .nc4 file generated by `make_cube()`
* **Output:** A cube object
* **Additional Arguments:** = None
* Example function call:

```python
# a cube object file
newCube = "myDirectory/myCubeFile.nc4"

# load the cube object back in
ds = load_cube(file = newCube)
```



## Example Workflow:

```python
import spacetimepy as sp

# input file names
file1 = "file1.tif"
file2 = "file2.tif"

data = [file1, file2]

# read data from list of files and make a spacetimepy file object
ds = read_data(data)
##########################################################################

# align the rasters to the same epsg codes and grid size
newObj = raster_align(data=ds)

# trim the rasters to the same greatest common bounding box
trimmed = raster_trim(newObj)

# create spacetimepy time object
yearObj = cube_time(start="2000", length=101, scale = "day")

# make the alinged file object into a cube with a time element (writes the new file to disk)
ds = make_cube(data = trimmed, fileName = "test.nc4", organizeFiles = "filestovar", timeObj = yearObj)

# scale time does basic temporal summary (here we are doing monthly means)
x = scale_time(cube=ds, scale="month", method="mean")

# selects ranges of time and/or slices at different scales 
# here we extract aprils between '2000-02-29' and '2000-04-30'
y = select_time(cube=x, range=['2000-02-29', '2000-04-30'], scale = "month", element=4)

# cube smasher does mathmatical/function operations on a cube or cubes (times 5)
answer = cube_smasher(eq = "a * c", a = y, c = 5, parentCube = y)

# plot the cube and output the data set in dataframe format that made the plot
t=plot_cube(cube=x, variable="B", type="space", summary = "max", showPlot = True)

# convert a cube into a dataframe
df = cube_to_dataframe(cube=x)

# write out our final cube as a .cd4 file
ds = make_cube(data = x, fileName = "testCube.nc4")

# pull in the file name of our newly created cube
newCube = "/Users/pburnham/Documents/GitHub/barra_python/testCube.nc4"

# load the cube object back in
ds = load_cube(file = newCube)


```


 


		 