from setuptools import setup, find_packages

packages = \
['spacetimeraster',
 "spacetimeraster.input",
 "spacetimeraster.graphics",
 "spacetimeraster.objects",
 "spacetimeraster.operations",
 "spacetimeraster.output",
 "spacetimeraster.scale",
 ]


setup(
    name='spacetimeraster',
    version='0.1.2',
    license='GNU GPLv3',
    author='P. A. Burnham et al.',
    author_email='alexburn17@gmail.com',
    install_requires=['pandas', "numpy", "gdal", "xarray", "psutil", "plotly_express", "netCDF4"],
    description='A toolkit for working with spatiotemporal data',
    packages = packages,
)

