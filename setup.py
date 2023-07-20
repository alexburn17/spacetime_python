from setuptools import setup, find_packages

packages = \
['spacetimepy',
 "spacetimepy.input",
 "spacetimepy.graphics",
 "spacetimepy.objects",
 "spacetimepy.operations",
 "spacetimepy.output",
 "spacetimepy.scale",
 ]


setup(
    name='spacetimepy',
    version='0.1.2',
    license='GNU GPLv3',
    author='P. A. Burnham et al.',
    author_email='alexburn17@gmail.com',
    install_requires=['pandas', "numpy", "gdal", "xarray", "psutil", "plotly_express", "netCDF4"],
    description='A toolkit for working with spatiotemporal data',
    packages = packages,
)

