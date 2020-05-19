# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
from dash import dependencies

external_stylesheets = ['https://raw.githubusercontent.com/plotly/dash-app-stylesheets/master/dash-analytics-report.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=['/assets/navbar.js'])
exploration_div = html.Div(id='exploration_div')
model_div = html.Div(id='model_div')
app.layout = html.Div([
    html.Div(
        style={'overflow': 'hidden', 'width': '8%'},
        id='navbar',
        children=[
            html.Ol([
                html.Li(children=[html.A(href='#data-exploration', children=["Eksploracja danych"])]),
                html.Li(children=[html.A(href='#model-features', children=["Właściwości modelu"])]),
            ])
        ]
    ),
    html.Div(style={'float': 'left', 'width': '8%', 'height': 1000}),
    html.Div(style={
        'border-left': '6px solid green',
        'height': '2000px',
        'float': 'left'
    }),
    html.Div(style={'float': 'left', 'width': '90%'},
             children=[
                 html.H2("Eksploracja danych", id='data-exploration'),
                 exploration_div,
                 html.H2("Właściwości modelu", id='model-features', style={'float': 'left', 'width': '100%'}),
                 model_div
             ])
    # html.Button('exploration', id='exploration_button', n_clicks=0),
    # html.Button('model', id='model_button', n_clicks=0),
    # exploration_div,
    # model_div
])
