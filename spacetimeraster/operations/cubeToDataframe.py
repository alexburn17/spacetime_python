import pandas as pd
import numpy as np


def cube_to_dataframe(cube):
    # load data
    ds = cube.get_data_array()

    # if 3d or 4d data
    if cube.get_shapeval() == 4:

        df = ds.to_dataframe(name="value", dim_order=["lat", "lon", "variables", "time"])
        df = df.reset_index()
        df['variables'] = df['variables'].astype('category')

    else:

        df = ds.to_dataframe(name="value", dim_order=["lat", "lon", "time"])
        df = df.reset_index()


    return df
