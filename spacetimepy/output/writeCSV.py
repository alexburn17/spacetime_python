import pandas as pd
from spacetimepy.operations.cubeToDataframe import cube_to_dataframe


def write_csv(cube=None, file_name=None):

    shapeval = cube.get_shapeval()
    df = cube_to_dataframe(cube)
    df = df.loc[df['value'] > 0]
    print("This will take a few seconds.")
    if shapeval == 4:
        final_df = None
        for var in pd.unique(df['variables']):
            temp_df = pd.DataFrame
            temp_df = df.loc[df['variables'] == var]
            temp_df = temp_df.drop('variables', axis=1)
            temp_df = temp_df.rename({'value': ('var_' + str(var))}, axis=1)

            if final_df is None:
                final_df = temp_df
            else:
                final_df = pd.merge(final_df, temp_df, on=['time', 'lat', 'lon'])
        final_df.to_csv(file_name, encoding='UTF8')
    else:
        df.to_csv(file_name, encoding='UTF8')
