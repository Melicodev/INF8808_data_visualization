#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 18:14:51 2023

@author: gallou

App initialization file
"""

import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State

from datetime import date, datetime

import preprocess
import main_viz
import bar
import radar
import pandas as pd

app = dash.Dash(__name__)
app.title = "" #TBD
server = app.server

# Read CSV files
stats = pd.read_csv('./assets/df_stats.csv')
tweets = pd.read_csv('./assets/df_tweets.csv')

# Preprocess data
stats = preprocess.convert_dates(stats)
tweets = preprocess.convert_dates(tweets)
start,end = preprocess.get_timeframe(stats)

app.layout = html.Div(className='content', children = [
    html.Header(children=[
        html.H1("Titre de l'app") #TBD
    ]),
    html.Main(className='', children=[
        html.Div(className='bandeau_dessous', children=[
            html.Div(className='selecteur_viz', children=[
                None
            ]),
            dcc.DatePickerRange(id='my-date-picker-range',  #selecteur de date pour la viz 4
                                min_date_allowed=start,
                                max_date_allowed=end,
                                start_date=start,
                                end_date=end
            )
        ]),
        # TODO : Can we regorganize this layout
        html.Div(className='main_vis', children=[
            html.Div([
                    dcc.Graph(
                        id='main_vis',
                        figure=main_viz.init_main_figure(stats)
                    )
                ], style={'width': '75%', 'display': 'inline-block'}),

                html.Div(
                    children=[
                        html.Div(id='panel',
                                children=[
                                    html.Div(['Influencial tweets'], style={
                                        'fontSize': '24px'}),
                                    html.Div(id='date_row', style={
                                        'fontSize': '20px',"margin-top": "6px"}),
                                    html.Div(id='index_var', style={
                                        'fontSize': '20px',"margin-top": "6px"}),
                                    html.Div(id='tweet_row', style={
                                        'fontSize': '16px'})])]
                    ,style={'width': '23%',
                            'display': 'inline-block',
                            'vertical-align': 'top',
                            'padding': '10px',
                            'border': '1px solid black',
                            'border-radius': '10px'})
        ]),
        dcc.Tabs(id='viz_selection', value='viz-2', children=[
            dcc.Tab(label='afficher viz 2', value='viz-2', children=[
                    html.Div([
                            dcc.Graph(
                                id='bar_vis',
                                figure=bar.init_bar_figure(stats)
                            )
                ], style={'width': '60%', 'display': 'inline-block'}),
                ]),
            # TODO : decide what we display in the labels
            dcc.Tab(label='afficher viz 3', value='viz-3', children=[
                    html.Div([
                            dcc.Graph(
                                id='radar_vis',
                                figure=radar.init_radar_figure(stats),
                                )
                            ])
            ])
        ]),

        html.Div(id='viz_to_display', children=[]), # rendered in the callback associated to the tabs
    ])
])

@app.callback(
    [Output('tweet_row', 'children'),
     Output('index_var', 'children'),
     Output('date_row', 'children')],
    [Input('main_vis', 'clickData')],
    [State('tweet_row', 'children'),
     State('index_var', 'children'),
     State('date_row', 'children')]
    )
def display_tweet(click, cur_tweet, cur_index, cur_date):
    # TODO : Can we hide the panel if a marker is not yet clicked ?
    ctx = dash.callback_context
    if not ctx.triggered:
        return [], [], []
    
    if (ctx.triggered[0]['prop_id'].split('.')[0]=='main_vis') & (ctx.triggered[0]['value']['points'][0]['curveNumber'] == 0):
        date =  ctx.triggered[0]['value']['points'][0]['x'] 
        tweet1, tweet2 = main_viz.get_tweet(date)
        
        output1 = html.Div([
                    html.P(tweet1),
                    html.P(tweet2, style={'margin-top': '0px', 'padding-top': '0px'})
                ], style={'line-height': '80%'})
        index_variation = stats[stats['timestamp']==date]['index_variation'].round(2).values[0]
        output2 = f'Index variation : {index_variation}'
        output3 = 'Date : ' + str(date)
        return output1, output2, output3
    else:
        return cur_tweet, cur_index, cur_date
    
@app.callback(
    [Output('main_vis', 'figure'),
     Output('bar_vis', 'figure'),
     Output('radar_vis', 'figure')],
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')]
)
def update_figures(start_date, end_date):

    # Select the timeframe from the data set
    df = preprocess.select_timeframe(stats, start_date, end_date)

    main_fig = main_viz.init_main_figure(df)
    bar_fig = bar.init_bar_figure(df)
    radar_fig = radar.init_radar_figure(df)

    return main_fig, bar_fig, radar_fig
