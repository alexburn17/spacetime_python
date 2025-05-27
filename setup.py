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

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='spacetimepy',
    version='0.1.7',
    license='GNU GPLv3',
    author='P. A. Burnham et al.',
    author_email='alexburn17@gmail.com',
    install_requires=['pandas', "numpy", "gdal", "xarray", "psutil", "plotly_express", "netCDF4"],
    description='A toolkit for working with spatiotemporal data',
    packages = packages,
    long_description=long_description,
    long_description_content_type='text/markdown',
)

