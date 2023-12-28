import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

import more_itertools as it
from plotly.subplots import make_subplots

import preprocess

def init_bar_figure(data):

    # preprocess data
    data = preprocess.get_bar_chart_data(data)

    fig = go.Figure()
    # TODO : Update the template to include our new theme and set the title
    fig.update_layout(
        dragmode=False,
        barmode='relative',
        title={
        'text': 'Lines per act',
        'xanchor': 'center',
        'yanchor': 'top'},
        yaxis_title='Lines (count)',
    )
    
    fig = go.Figure(fig)  # conversion back to Graph Object
    
    fig.data = [] 
    ### ajout de hovertemplate pour prendre en compte l'info-bulle
    fig = px.bar(data, x='sum_influence_3_days', y='Count',
                 color='variation',
                 title='Distribution of activity',
                 height=400)
    
    fig.update_layout(legend_title='Type of variation')
    fig.update_xaxes(title='Activity (3-Days Influence)')
    fig.update_yaxes(title='Count')

    return fig
