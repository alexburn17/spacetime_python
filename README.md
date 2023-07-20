

![spacetimepy logo](/Users/pburnham/Desktop/barracudaDocumentation/barraLogo.jpg)


-----------------

# spacetimepy: A user-friendly tool for working with spatiotemporal data.

## About spacetimepy

The main objective of the spacetimepy python library is to make tasks like loading, rescaling, merging, and conducting mathmatical operations on spatiotemporal (or other D-dimensional data sets) easier for the user by providing a set of concise yet powerful functions. spacetimepy opperations utilize a cube-like structure for all data sets that makes storing and manipulating large D-dimensional datasets more efficient. For scientists working with spatiotemporal data (such as climate or weather data sets) spacetimepy is an ideal platform that allows the user to focus on the science rather than the coding.

## Main Functionality
spacetimepy is in the beta stage (version number = 0.0.1) and additional functionality will be added on a regular basis. The current functionality of spacetimepy is below:

- raster_align: aligns a set of raster file to a common grid size and EPSG code.
- raster_trim: Trims a set of raster files to the largest common bounding box.
- get_coords: Returns an array of the coordinates (latidute and longitude) for any raster file type.
- cuberator: Writes a spacetimepy dataset to a specified file type.
- cube_smasher: Takes a set of raster files or D-dimensional arrays, scales them to a common scale and conducts a user defined mathmatical operation or  function call.
- visulize: takes a spacetimepy data set and plots a series of basic figures.

## A Simple Example

In the following example, two .tif files with different spatial scales are passed to the cube smasher function, which rescales them to a common grid, and conducts the following mathmatical operation where a and b are the 3 dimensional data sets contained in the .tif files and c is a constant scaler value of 5:

<math display="block">
 <mrow>
  <mi>a</mi>
  <mo>+</mo>
  <msup>
   <mi>b</mi>
   <mi>c</mi>
  </msup>
 </mrow>
     <mo>=</mo>
    <mi>result</mi>
 
</math>

```python

# paths to tif files with different spatial grid sizes
path1 = "/Users/pburnham/Documents/geospatialData/Carya_ovata/Carya_ovata_sim_disc_1km.tif"
path2 = "/Users/pburnham/Documents/geospatialData/Carya_ovata/Carya_ovata_sim_disc_10km.tif"

# mathmatical operations on two netCDF files of different scales
y, coords = cube_smasher(eq = "a + b ** c", a=path1, b=path2, c = 5, fromFiles = True)

```

The function returns the new cube data set as a numpy array as well as the latitude and longitude cordinates. 

## Documentation

The full documentation for this library may be found at https://biobarricuda.com/software/spacetimepy-documentation


## Dependancies

- spacetimepy relies on the Python bindings of GDAL for most of its geographic rescalling functionality.
- spacetimepy ustilizes the netCDF4 library for storing and passing data sets between functions.


## Installation

The source code may be found on Github at (my github repo for spacetimepy)

The latest version of spacetimepy may be installed from the [Python
Package Index (PyPI)](https://pypi.org/project/pandas).

```sh
pip install spacetimepy
```


## Authors

- P. Alexander Burnham
- Brian McGill
- Nicholas Gotelli
- Matt Dube

