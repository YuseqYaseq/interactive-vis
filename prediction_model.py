import json

import dash
import dash_html_components as html
import dash_core_components as dcc
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Output, Input

from app import app
from cursor import cursor, voivodeships

html_elements = []

#bg_color = '#F9DEC9'
bg_color = '#C2EABD'
font_settings = {'color': '#000000',
                 'size': 10}
continous_color_sequence = 'Fall'
discrete_color_sequence = ['#D4AA7D', '#967D69', '#92B9BD', '#272727']


def create_table(array):
    return html.Table(
        [html.Tr([html.Th([array[i, j]]) for j in range(array.shape[1])]) for i in range(array.shape[0])],
        style={'float': 'left', 'width': '100%'}
    )


def get_pred_error(output, true_y):
    return [(1 - output[i][int(v)]) for i, v in enumerate(true_y)]


def get_scatter_figure(x, col1, col2):
    return {
        'data': [dict(
            x=x[x['Target'] == i][col2],
            y=x[x['Target'] == i][col1],
            text=x[x['Target'] == i]['MainAddressCounty'],
            mode='markers',
            opacity=0.8,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i) for i in [True, False]],
        'layout': dict(
            xaxis={'type': 'log', 'title': col1},
            yaxis={'type': 'log', 'title': col2},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
        )
    }
