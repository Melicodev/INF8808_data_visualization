'''
    Contains the functions to set up the map visualization.

'''

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

import preprocess
import hover_template

def init_radar_figure(data):
    # TODO : Can we add a figure for the avarage activity per hour (amount of tweets and/or followers)

    # Get the start and end dates for the title
    start, end = preprocess.get_timeframe(data)

    # prepare the avarage data set
    mean_df = preprocess.get_radar_trend_data(data)

    # prepare the scatter data set
    scatter_data = preprocess.get_radar_scatter_data(data)

    # Create the figures
    fig = go.Figure()
    fig = add_radar_trend_figure(fig, mean_df)
    fig = add_radar_scatter_figure(fig, scatter_data)

    # Customize layout
    fig.update_layout(polar=dict(angularaxis=dict(tickvals=np.arange(0,360,15),
                                            ticktext=[str(x) for x in np.arange(24)],
                                            showticklabels=True,
                                            showline=False,
                                            showgrid=False,
                                            linewidth=3,
                                            ticks='inside',
                                            direction='clockwise'
                                            ),
                                radialaxis = dict(
                                            ticktext=[str(x) for x in np.arange(24)],
                                            showticklabels=True,
                                            ticks='',
                                            showline=True,
                                            showgrid=True,
                                            gridcolor='white',
                                            tickfont=dict(size=4)
                                            )),
                     template=None
                )

    # Add dropdown
    fig.update_layout(
        title="Hourly visualisation of the index variation <br><sup>{} to {}</sup>".format(start, end),
        updatemenus=[
            dict(
                type = "buttons",
                direction = "left",
                buttons=list([
                    dict(
                        args = [{'visible': [True, False]}],
                        label="Trend",
                        method="update"
                    ),
                    dict(
                        args = [{'visible': [False, True]}],
                        label="Scatter",
                        method="update"
                    )
                ]),
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.5,
                xanchor="center",
                y=-0.25,
                yanchor="bottom"
            ),
        ],
        #legend = {"xanchor": "left", "x": 0}
        legend=dict(traceorder='normal',  # include legend within maximum width
                    x=0.4,  # set x position of legend within plot
                    )
    )

    return fig

def add_radar_scatter_figure(fig, scatter_data):

    scatter = go.Scatterpolar(r=scatter_data["variation"], theta=scatter_data["hour_angle"], 
                              mode='markers',
                              marker=dict(color=scatter_data["count"],
                                          colorscale='Viridis',
                                          colorbar=dict(title="Frequency"),
                                          showscale=True),
                              hovertemplate=hover_template.get_radar_scatter_hover_template(),
                              visible=False)

    fig.add_trace(scatter)

    return fig

def add_radar_trend_figure(fig, mean_df):

    trend = go.Scatterpolar(r=mean_df["index_variation"], theta=mean_df["hour_angle"], mode='lines',
                                connectgaps=True,
                                hovertemplate=hover_template.get_radar_trend_hover_template())

    fig.add_trace(trend)
    
    return fig