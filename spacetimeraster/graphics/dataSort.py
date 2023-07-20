# Sorting methods for control chart output.
import pandas
import pandas as pd
import numpy as np

from typing import Tuple, List

from spacetimeraster.operations.cubeToDataframe import cube_to_dataframe


# Main Method
########################################################################################################################
# Process Cube data for chart plotting
def organize_dataframe(cube, plot_type, variable, summary) -> pd.DataFrame:
    df = cube_to_dataframe(cube)
    shape_val = cube.get_shapeval()

    if shape_val == 4:
        if plot_type == "space":
            if variable is None:
                df_temp = df[df['variables'] == df['variables'][0]]
            else:
                df_temp = df[df['variables'] == variable]
        else:
            df_temp = df
    else:
        df_temp = df

    df_plot = df_temp.where(df_temp != cube.get_nodata_value())
    summ_df = pd.DataFrame

    if plot_type != 'space':
        if shape_val == 4:
            if summary == "mean":
                summ_df = df_plot.groupby(["time", "variables"]).mean().reset_index()
            if summary == "median":
                summ_df = df_plot.groupby(['time', "variables"]).median().reset_index()
            if summary == "min":
                idx = df_plot.groupby(['time', 'variables'])['value'].idxmin()
                summ_df = df_plot.loc[idx]
            if summary == "max":
                idx = df_plot.groupby(['time', 'variables'])['value'].idxmax()
                summ_df = df_plot.loc[idx]
        else:
            if summary == "mean":
                summ_df = df_plot.groupby('time').mean().reset_index()
            if summary == "median":
                summ_df = df_plot.groupby('time').median().reset_index()
            if summary == "min":
                idx = df_plot.groupby(['time'])['value'].idxmin()
                summ_df = df_plot.loc[idx]
            if summary == "max":
                idx = df_plot.groupby(['time'])['value'].idxmax()
                summ_df = df_plot.loc[idx]
    else:
        summ_df = df_plot

    summ_df.insert(loc=0, column='timeChar', value=summ_df['time'].astype(str))
    summ_df.insert(loc=0, column='year', value=pd.DatetimeIndex(summ_df['time']).year)

    return summ_df


# sort data for control chart
def sort_dataframe(
        df: pandas.DataFrame,
        show_avg="all",
        show_deviations="all",
        deviation_coefficient=1,
        show_trends="updown",
) -> Tuple[pandas.DataFrame, List]:

    df_sorted = df
    segments = []

    std = np.std(df['value'])
    avg = get_avg(df)

    if show_avg != 'none':

        df_sorted['above_avg_mask'] = np.where(df['value'].values >= avg, 1, 0)
        df_sorted['below_avg_mask'] = np.where(df['value'].values < avg, 1, 0)

    if show_deviations != 'none':

        df_sorted['deviation_above_mask'] = np.where(
            df['value'].values >= (avg + (std * deviation_coefficient)), 1, 0
        )
        df_sorted['deviation_below_mask'] = np.where(
            df['value'].values < (avg - (std * deviation_coefficient)), 1, 0
        )

    if show_trends != 'none':
        segments = sort_trends(df)

    return df_sorted, segments


# Helper methods
########################################################################################################################
def sort_trends(df) -> List:
    min_change = 10
    curr_changes = 0
    last_sign = 1
    last_change_idx = 0
    bounds_idx = [0]
    cumulative_slope = [0]

    df['row'] = np.arange(len(df))

    # for each data point, calculate the slope of the linear regression that includes all the data points before it
    for i in range(1, df.shape[0]):
        segment = df.iloc[0:i + 1, :]

        slope = calc_slope(segment)
        cumulative_slope.append(slope)

        # compare the current cumulative slope with the previous, and keep track of whether it increased or decreased
        # as well as how many times it has changed in that direction, and where it last changed direction
        if abs(cumulative_slope[i]) < abs(cumulative_slope[i - 1]):
            if last_sign == 1:
                curr_changes = 0
            if curr_changes == 0:
                last_change_idx = i
            curr_changes += 1
            last_sign = -1

        elif abs(cumulative_slope[i]) > abs(cumulative_slope[i - 1]):
            if last_sign == -1:
                curr_changes = 0
            if curr_changes == 0:
                last_change_idx = i
            curr_changes += 1
            last_sign = 1

        # if we meet the minimum amount of times the slope changes in a direction, mark the last time it changed
        # and reset the change counter
        if curr_changes == min_change:
            curr_changes = 0
            bounds_idx.append(last_change_idx)

    # add the last point in the dataset to the bounds just to ensure we encapsulate all points
    bounds_idx.append(df.shape[0] - 1)
    return bounds_idx


def get_avg(df):
    return np.average(df['value'].values)


def calc_slope(df):
    slope = np.polyfit(df['row'], df['value'], 1)
    return slope[0]
