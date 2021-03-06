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
                html.Ol(children=[
                    html.Li(children=[html.A(href='#pie-charts', children=["Dwuwartościowe cechy działalności a jej kontynuowanie"])]),
                    html.Li(children=[html.A(href='#by-month', children=["Działalności kontynuowane i niekontynuowane w rozłożeniu na miesiące rozpoczęcia działalności"])])
                ]),
                html.Li(children=[html.A(href='#model-features', children=["Właściwości modelu"])]),
            ])
        ]
    ),
    html.Div(style={'float': 'left', 'width': '8%', 'height': 1000}),
    html.Div(style={
        'border-left': '6px solid green',
        'margin-right': '12px',
        'height': '2000px',
        'float': 'left'
    }),
    html.Div(style={'float': 'left', 'width': '90%'},
             children=[
                 html.H1("Eksploracja danych", id='data-exploration'),
                 exploration_div,
                 html.H1("Właściwości modelu", id='model-features', style={'float': 'left', 'width': '100%'}),
                 model_div
             ])
])
