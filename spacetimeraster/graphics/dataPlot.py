# File Header includes imports and constants
########################################################################################################################
import numpy as np
import pandas as pd
import plotly_express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from typing import Optional, Union, Tuple

import statsmodels.api as sm
import datetime
import math

from spacetimeraster.graphics.dataSort import sort_dataframe, organize_dataframe

# Style color presets
COLOR_STYLES = {
    "chart_background": "#222831",
    "chart_grid": "#41434a",
    "tick_font": "#bbbbbb",
    "font": "#bbbbbb",
    "line_colors": [
        "#777777"
    ],
    "marker_colors": [
        "#00FFFF",
        "#FF00FF",
        "#FFFF00",
        "#0000FF",
        "#00FF00",
        "#FF0000",
    ]
}

# flags for data styling.
FLAGS = {
    "base": ["Base", COLOR_STYLES["line_colors"][0]],
    "above_avg": ["Above Average", COLOR_STYLES["marker_colors"][0]],
    "below_avg": ["Below Average", COLOR_STYLES["marker_colors"][1]],
    "deviation_above": ["Deviation Above", COLOR_STYLES["marker_colors"][2]],
    "deviation_below": ["Deviation Below", COLOR_STYLES["marker_colors"][3]],
    "trending_up": ["Trending Up", COLOR_STYLES["marker_colors"][4]],
    "trending_down": ["Trending Down", COLOR_STYLES["marker_colors"][5]],
}
########################################################################################################################


# Primary Methods
########################################################################################################################
# Main Plotting method, delegates plotting to sub-methods and returns a completed plotly figure.
def plot_cube(
        cube,
        plot_type: str = "timeseries",
        variable: Optional[Union[str, int]] = None,
        summary: str = "mean",
        show_avg: str = "all",
        show_deviations: str = "all",
        deviation_coefficient: int = 1,
        show_trends: str = "updown",
        histo_type: str = "single",
        histo_highlight: str = 'variable',
        discrete_latlong_size: Union[int, float] = 10,
        bin_size: Union[int, float] = 100,
        show_plot: bool = True,
) -> go.Figure:

    """
    Parameter Definitions:

        cube: <accepted types: cube object>
                A cube object.

        plot_type: <accepted types: string>
                The type of plot to output.
                Options:
                    'space' - creates a choropleth heatmap
                    'timeseries' - creates a line plot
                    'control' - creates a configurable control chart plot
                    'histogram' - creates a configurable histogram plot
                    'box' - creates a box plot

        variable: <accepted types: string, integer>
                The variable name to filter the dataset by.

        summary: <accepted types: string>
                The aggregation function for the dataset.
                Options:
                    'min' - aggregates by the minimum value
                    'max' - aggregates by the maximum value
                    'median' - aggregates by the median value
                    'mean' - aggregates by the mean value

        show_avg: <accepted types: string>
                For use with Control Charts, allows toggling of highlighting for average values.
                Options:
                    'above' - highlights markers above average
                    'below' - highlights markers below average
                    'all' - combines 'above' and 'below' options
                    'none' - no average based highlighting

        show_deviations: <accepted types: string>
                For use with Control Charts, allows toggling of highlighting for standard deviation
                values. Related: deviation_coefficient
                Options:
                    'above' - highlights markers in positive standard deviation
                    'below' - highlights markers in negative standard deviation
                    'all' - combines 'above' and 'below' options
                    'none' - no deviation based highlighting

        deviation_coefficient: <accepted types: integer>
                For use with Control Charts, set how many standard deviations outside the data set
                normal you want to count for show_deviations highlighting. Related: show_deviations

        show_trends: <accepted types: string>
                For use with Control Charts, allows toggling of trendlines.
                Options:
                    'all' - show all trendlines regardless of p-value
                    'up' - show p-value significant trendlines for positive trends
                    'down' - show p-value significant trendlines for negative trends
                    'updown' - combines 'up' and 'down' options
                    'none' - show no trendlines

        histo_type: <accepted types: string>
                For use with Histograms, determines histogram output type. Related: bin_size
                Options:
                    'single' - a single histogram chart
                    'multi' - a histogram chart for each unique variable in the data set
                    'animated' - a histogram chart that animates over the time series of the data set

        histo_highlight: <accepted types: string>
                For use with Histograms, determines additional highlighting for histogram charts.
                Related: discrete_latlong_size
                Options:
                    'variable' - highlights bins based on which variable the value belongs to.
                                    alias: 'var', 'variables'
                    'latitude' - highlights bins based on the latitude degree range the value was measured in.
                                    alias: 'lat'
                    'longitude' - highlights bins based on the longitude degree range the value was measured in.
                                    alias: 'lon', 'long'
                    'none' - no special highlighting.

        discrete_latlong_size: <accepted types: integer, float>
                For use with Histograms, determines the size in degrees of the distinctions for latitude and
                longitude based highlighting. Related: histo_highlight

        bin_size: <accepted types: integer, float>
                For use with Histograms, determined the bin size of animated histograms. Related: histo_type

        show_plot: <accepted types: boolean>
                Allows the user to turn off automatic chart output.
    """

    df_plot = organize_dataframe(cube, plot_type, variable, summary)

    input_validity = validate_inputs(df_plot,
                                     plot_type,
                                     #variable,
                                     summary,
                                     show_avg,
                                     show_deviations,
                                     show_trends,
                                     histo_type,
                                     histo_highlight,
                                     )

    if input_validity:
        fig = go.Figure

        if plot_type == 'space':
            fig = plot_spatial(cube, df_plot)

        elif plot_type == 'timeseries':
            fig = plot_timeseries(df_plot)

        elif plot_type == 'control':
            fig = plot_control(df_plot, show_avg, show_deviations, deviation_coefficient, show_trends)

        elif plot_type == 'histogram':
            fig = plot_histogram(df_plot, histo_type, histo_highlight, discrete_latlong_size, bin_size)

        elif plot_type == 'box':
            fig = plot_box(df_plot, variable)

        if show_plot:
            fig.show()

    return fig
########################################################################################################################


# Secondary cube plotting methods
########################################################################################################################
# Plot a spatial choropleth chart
def plot_spatial(cube, df) -> go.Figure:
    time = df["timeChar"]

    # Max value for legend
    max_val = np.nanmax(df["value"])
    min_val = np.nanmin(df["value"])

    coords = cube.get_UL_corner()

    fig = px.scatter_mapbox(
        df,
        lat='lat',
        lon='lon',
        color='value',
        animation_frame=time,
        range_color=(min_val, max_val),
        color_continuous_scale='Viridis',
        opacity=0.5,
    )

    fig.update_layout(
        mapbox_style='carto-darkmatter',
        mapbox_zoom=3,
        mapbox_center={'lat': float(coords[0]), 'lon': float(coords[1])},
    )

    fig = update_fig_layout(fig)

    return fig


# Plot a time series chart
def plot_timeseries(df) -> go.Figure:
    time = df['timeChar']

    if 'variables' in df.columns:
        fig = px.line(df, x=time, y="value", color='variables')
    else:
        fig = px.line(df, x=time, y="value")

    fig = update_fig_layout(fig)

    return fig


# Plot a control chart
def plot_control(df, show_avg, show_deviations, deviation_coefficient, show_trends) -> go.Figure:
    # Additional processing necessary for control chart plotting.
    df_plot, segments = sort_dataframe(
        df,
        show_avg=show_avg,
        show_deviations=show_deviations,
        deviation_coefficient=deviation_coefficient,
        show_trends=show_trends
    )

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_plot['time'],
        y=df_plot['value'],
        mode='lines',
        line=dict(color=FLAGS['base'][1]),
        showlegend=False,
    ))  # Base line plot

    # Filter dataset and select the relevant style options for each trace.
    for key in FLAGS.keys():
        if show_avg != 'none':
            if key == 'above_avg' and show_avg != 'below':
                marker_name = FLAGS[key][0]
                marker_color = FLAGS[key][1]
                fig = add_markers(df_plot.loc[df_plot['above_avg_mask'] == 1], fig, marker_name, marker_color)
            if key == 'below_avg' and show_avg != 'above':
                marker_name = FLAGS[key][0]
                marker_color = FLAGS[key][1]
                fig = add_markers(df_plot.loc[df_plot['below_avg_mask'] == 1], fig, marker_name, marker_color)

        if show_deviations != 'none':
            if key == 'deviation_above' and show_deviations != 'below':
                marker_name = FLAGS[key][0]
                marker_color = FLAGS[key][1]
                fig = add_markers(df_plot.loc[df_plot['deviation_above_mask'] == 1], fig, marker_name, marker_color)
            if key == 'deviation_below' and show_deviations != 'above':
                marker_name = FLAGS[key][0]
                marker_color = FLAGS[key][1]
                fig = add_markers(df_plot.loc[df_plot['deviation_below_mask'] == 1], fig, marker_name, marker_color)

    # Add trend traces to chart.
    if show_trends != 'none':
        for start_idx, end_idx in zip(segments[:-1], segments[1:]):
            segment = df_plot.iloc[start_idx:end_idx + 1, :].copy()

            # Serialize the time value since we can't do linear regressions on datetime64[ns]
            segment['serial_time'] = [(d - datetime.datetime(1970, 1, 1)).days for d in segment['time']]

            x = sm.add_constant(segment['serial_time'])
            model = sm.OLS(segment['value'], x).fit()
            segment['fitted_values'] = model.fittedvalues

            fit_color = COLOR_STYLES['marker_colors'][4] if model.params['serial_time'] > 0 \
                else COLOR_STYLES['marker_colors'][5]

            trend_name = "Trending Up" if model.params['serial_time'] > 0 else "Trending Down"

            # Determine if the current trace should be added to the figure.
            print_trend = False

            if show_trends == 'all':
                print_trend = True
            else:
                if model.f_pvalue < 0.05:
                    if show_trends == 'up' and model.params['serial_time'] > 0:
                        print_trend = True
                    elif show_trends == 'down' and model.params['serial_time'] <= 0:
                        print_trend = True
                    elif show_trends == 'updown':
                        print_trend = True
                    else:
                        pass
                else:
                    pass

            if print_trend:
                fig.add_trace(go.Scatter(
                    x=segment['time'],
                    y=segment['fitted_values'],
                    mode='lines',
                    line=dict(color=fit_color),
                    name=trend_name,
                ))

        # Ensure duplicate legend items don't get added.
        legend_names = set()
        fig.for_each_trace(
            lambda trace:
            trace.update(showlegend=False) if (trace.name in legend_names) else legend_names.add(trace.name)
        )

    return fig


# Plot a Histogram of the chart data
def plot_histogram(df_plot, histo_type, histo_highlight, discrete_latlong_size, bin_size) -> go.Figure:
    fig = go.Figure()

    # Quickly check if the dataset has variables or not.
    has_vars = False

    if 'variables' in df_plot.columns:
        has_vars = True
        variables = list(pd.unique(df_plot['variables']))

    years = list(pd.unique(df_plot['year']))

    variable_alias = ['var', 'variables', 'variable']
    latitude_alias = ['lat', 'latitude']
    longitude_alias = ['lon', 'long', 'longitude']

    # Create categories in the data to highlight geographically.
    if histo_highlight in latitude_alias or histo_highlight in longitude_alias:
        bins, bins_labels = make_bins(discrete_latlong_size, bin_min=-90.0, bin_max=90.0)
        if histo_highlight in latitude_alias:
            df_plot['bins'] = pd.cut(x=df_plot['lat'], bins=bins, labels=bins_labels)
        elif histo_highlight in longitude_alias:
            df_plot['bins'] = pd.cut(x=df_plot['lon'], bins=bins, labels=bins_labels)

    # Singular Histogram chart output
    if histo_type == 'single':
        if histo_highlight in variable_alias and has_vars is True:
            for variable in variables:
                trace = construct_histo_trace(df=df_plot, filters=[variable], highlight='variable')
                trace['name'] = f"variable: {variable}"
                fig.add_trace(trace)
            fig.update_layout(barmode='stack')

        elif histo_highlight in latitude_alias or histo_highlight in longitude_alias:
            for bins in pd.unique(df_plot['bins']):
                trace = construct_histo_trace(df=df_plot, filters=[bins], highlight='geographic')
                trace['name'] = f"{histo_highlight}: {bins}"
                fig.add_trace(trace)

            fig.update_layout(barmode='stack')
        else:
            fig = px.histogram(x=df_plot['value'])

    # Histogram Chart Output with subplots.
    elif histo_type == 'multi':

        if has_vars is True:
            subplot_count = len(variables)
            subplot_col = 2
            subplot_row = math.ceil(subplot_count / 2)
            variable_count = 0
            fig = make_subplots(rows=subplot_row, cols=subplot_col)

            for col in range(0, subplot_col):
                for row in range(0, subplot_row):
                    if variable_count <= len(variables):
                        if histo_highlight in variable_alias or histo_highlight == 'none':
                            trace = construct_histo_trace(
                                df=df_plot,
                                filters=[variables[variable_count]],
                                highlight='variable'
                            )
                            trace['name'] = f"variable: {variables[variable_count]}"
                            fig.add_trace(trace, row=row + 1, col=col + 1)
                            fig.update_layout(barmode='stack')

                        elif histo_highlight in latitude_alias or histo_highlight in longitude_alias:
                            for bins in pd.unique(df_plot['bins']):
                                trace = construct_histo_trace(df=df_plot,
                                                              filters=[bins, variables[variable_count]],
                                                              highlight='geographic')
                                trace['name'] = f"variable: {variables[variable_count]}, {histo_highlight}: {bins}"
                                fig.add_trace(trace, row=row + 1, col=col + 1)

                            fig.update_layout(barmode='stack')
                        else:
                            raise ValueError(f"{histo_highlight} is not a valid highlight.")
                        variable_count += 1
        else:
            raise ValueError("Multi histograms only available if cube contains multiple variables.")

    # Animated Histogram Chart by Year.
    elif histo_type == 'animated':
        fig_frames = []
        max_bin = 0
        view_padding = df_plot['value'].max() * 0.05 if df_plot['value'].max() > 0 else 1
        view_max = df_plot['value'].max() + view_padding
        view_min = df_plot['value'].min() - view_padding

        # Make Slider
        sliders_dict = {
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 20},
                "prefix": "Year:",
                "visible": True,
                "xanchor": "right"
            },
            "transition": {"duration": 300, "easing": "cubic-in-out"},
            "pad": {"b": 10, "t": 50},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": []
        }

        # Making Frames
        for year in years:

            frame_data = []

            # For variable highlighting
            if histo_highlight in variable_alias:
                for variable in variables:

                    df_plot_of_year_by_var = df_plot['value'].loc[(df_plot['year'] == year) & (df_plot['variables'] == variable)]

                    data = {
                        'type': 'histogram',
                        'x': np.array(df_plot_of_year_by_var),
                        'name': str(variable),
                        'showlegend': True
                    }
                    frame_data.append(data)
                    absolute_max_bin = df_plot_of_year_by_var.shape[0]
                    max_bin = max(max_bin, absolute_max_bin)

            # For geographical highlighting
            if histo_highlight in latitude_alias or histo_highlight in longitude_alias:
                for bins in pd.unique(df_plot['bins']):

                    df_plot_of_year_by_bins = df_plot['value'].loc[(df_plot['year'] == year) & (df_plot['bins'] == bins)]

                    data = {
                        'type': 'histogram',
                        'x': np.array(df_plot_of_year_by_bins),
                        'name': f"{histo_highlight}: {bins}",
                        'showlegend': True
                    }
                    frame_data.append(data)
                    absolute_max_bin = df_plot_of_year_by_bins.shape[0]
                    max_bin = max(max_bin, absolute_max_bin)

            # For no highlighting
            if histo_highlight == 'none':

                df_plot_of_year = df_plot.loc[df_plot['year'] == year]

                data = {
                    'type': 'histogram',
                    'x': df_plot_of_year['value'],
                    'showlegend': False
                }
                frame_data.append(data)
                absolute_max_bin = df_plot_of_year.shape[0]
                max_bin = max(max_bin, absolute_max_bin)

            frame = go.Frame(data=frame_data, name=str(year))

            fig_frames.append(frame)

            slider_step = {"args": [
                [year],
                {"frame": {"duration": 300, "redraw": True},
                 "mode": "immediate",
                 "transition": {"duration": 300}}
            ],
                "label": str(year),
                "method": "animate"}
            sliders_dict["steps"].append(slider_step)

        # Making the final Plot and Layout
        fig = go.Figure(
            data=fig_frames[0]['data'],
            layout=go.Layout(
                xaxis=dict(
                    range=[view_min, view_max],
                    autorange=False
                ),
                yaxis=dict(
                    range=[0, max_bin + (0.05 * max_bin)],
                    autorange=False
                ),
                title="Histogram animated",
                updatemenus=[
                    dict(
                        type="buttons",
                        buttons=[dict(label="Play",
                                      method="animate",
                                      args=[None, {"frame": {"duration": 500, "redraw": True},
                                                   "fromcurrent": True,
                                                   "transition": {"duration": 300}}]
                                      ),
                                 dict(
                                     label="Pause",
                                     method="animate",
                                     args=[[None], {"frame": {"duration": 0, "redraw": True},
                                                    "mode": "immediate",
                                                    "transition": {"duration": 0}}]
                                 )],
                        showactive=False,
                    )
                ],
                sliders=[sliders_dict],
                barmode='stack'
            ),
            frames=fig_frames
        )

        # Keep the scale consistent across frames, so that we don't end up with bins too large or too small.
        rounded_bounds = (round(df_plot['value'].max(), -3) - round(df_plot['value'].min(), -3))
        bin_count = rounded_bounds / bin_size

        fig.update_traces(xbins=dict(
                              start=view_min,
                              end=view_max,
                              size=(rounded_bounds / bin_count) if bin_count > 0 else 0.5
                          ))

    return fig


# Make a box plot
def plot_box(df, variable) -> go.Figure:
    fig = go.Figure()

    if 'variables' in df.columns:
        if variable is None:
            var_opts = pd.unique(df['variables'])
        else:
            var_opts = variable

        for var in var_opts:
            fig.add_trace(go.Box(
                x=df['variables'].loc[df['variables'] == var],
                y=df['value'].loc[df['variables'] == var],
                name=f"variable: {var}",
                showlegend=True
            ))
    else:
        fig.add_trace(go.Box(
            y=df['value'],
            showlegend=True
        ))

    return fig


# Helper methods
########################################################################################################################
# Create Histogram Trace
def construct_histo_trace(df, bins=None, filters=[], highlight=''):
    trace = []
    filtered_df = pd.DataFrame()

    if highlight == 'variable':
        filtered_df = df['value'].loc[df['variables'] == filters[0]]

    elif highlight == 'geographic':
        if len(filters) > 1:
            filtered_df = df.loc[(df['bins'] == filters[0]) & (df['variables'] == filters[1])]
        else:
            filtered_df = df.loc[df['bins'] == filters[0]]

    trace = go.Histogram(x=filtered_df)

    return trace


# Add trace for control chart
def add_markers(df, fig, marker_name, marker_color) -> go.Figure:
    fig.add_trace(go.Scatter(
        x=df['time'],
        y=df['value'],
        mode='markers',
        name=marker_name,
        marker_color=marker_color,
    ))

    return fig


# Chart Figure layout update
def update_fig_layout(fig) -> go.Figure:
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 20, "b": 0},
        plot_bgcolor='#252e3f',
        paper_bgcolor='#252e3f',
        font=dict(color='#7fafdf'),
    )

    return fig


# Make bin list for histogram
def make_bins(bin_size, bin_min, bin_max) -> Tuple[list, list]:
    bins = []
    bins_labels = []
    bin_val = bin_min
    previous_bin = bin_min

    while bin_val <= bin_max:
        bins.append(bin_val)
        if bin_val > bin_min:
            bins_labels.append(f"{previous_bin + 0.1} to {bin_val}")
        previous_bin = bin_val
        bin_val += bin_size

    if bin_val > bin_max and bin_max not in bins:
        bins.append(bin_max)
        bins_labels.append(f"{previous_bin + 0.1} to {bin_max}")

    return bins, bins_labels


# Validate the user input so that we catch invalid parameter arguments before doing a lot of work.
def validate_inputs(
        df,
        plot_type,
        #variable,
        summary,
        show_avg,
        show_deviations,
        show_trends,
        histo_type,
        histo_highlight,
) -> bool:

    # Dictionary of valid parameter arguments
    valid_args = {
        #'variables': pd.unique(df['variables']),
        'plot_type': ['space', 'timeseries', 'control', 'histogram', 'box'],
        'summary': ['min', 'max', 'mean', 'median'],
        'show_avg': ['above', 'below', 'all', 'none'],
        'show_deviations': ['above', 'below', 'all', 'none'],
        'show_trends': ['up', 'down', 'updown', 'all', 'none'],
        'histo_type': ['single', 'multi', 'animated'],
        'histo_highlight': ['var', 'variable', 'variables', 'lat', 'latitude', 'lon', 'long', 'longitude', 'none'],
    }

#     # Variable selection
#     if variable not in valid_args['variables'] and variable is not None:
#         raise ValueError(
#             f"{variable} does not exist in the 'variables' field. Variables are: {valid_args['variables']}"
#         )

    # Plot type selection
    if plot_type not in valid_args['plot_type']:
        raise ValueError(
            f"{plot_type} is not a valid plot type. Options are: {valid_args['plot_type']}"
        )

    # Aggregation method selection
    if summary not in valid_args['summary']:
        raise ValueError(
            f"{summary} is not a valid summary function. Options are: {valid_args['summary']}"
        )

    # Control Chart arguments
    if show_avg not in valid_args['show_avg']:
        raise ValueError(
            f"{show_avg} not a valid average highlight option. Options are: {valid_args['show_avg']}"
        )
    if show_deviations not in valid_args['show_deviations']:
        raise ValueError(
            f"{show_deviations} not a valid deviations highlight option. Options are: {valid_args['show_deviations']}"
        )
    if show_trends not in valid_args['show_trends']:
        raise ValueError(
            f"{show_trends} not a valid trends highlight option. Options are: {valid_args['show_trends']}"
        )

    # Histogram arguments
    if histo_type not in valid_args['histo_type']:
        raise ValueError(
            f"{histo_type} not a valid histogram chart type. Options are: {valid_args['histo_type']}"
        )
    if histo_highlight not in valid_args['histo_highlight']:
        raise ValueError(
            f"{histo_highlight} not a valid histogram highlight option. Options are: {valid_args['histo_highlight']}"
        )

    return True
