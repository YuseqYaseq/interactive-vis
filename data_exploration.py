import dash_html_components as html
import dash_core_components as dcc
from dash import dependencies
import plotly.express as px

from app import app
from cursor import Cursor

html_elements = []

data = Cursor()
html_elements.append(html.Div([
    dcc.Graph(
        id='graph1',
        figure={
            'data': [dict(
                x=data.get1(i)[0],
                y=data.get1(i)[1],
                text=data.get1(i)[2],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
                ) for i in [True, False]],
            'layout': dict(
                xaxis={'type': 'log', 'title': 'Czas istnienia spółki [msc]'},
                yaxis={'title': 'Liczba unikalnych PKD'},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            ),
        },
    ),
    html.Button('0', id='button0', n_clicks=0),
],))


@app.callback(
    dependencies.Output('graph1', 'figure'),
    [dependencies.Input('button0', 'n_clicks')]
)
def update_graph(b0):

    if b0 % 3 == 0:
        tab = [True, False]
    elif b0 % 3 == 1:
        tab = [True]
    elif b0 % 3 == 2:
        tab = [False]

    return {
        'data': [dict(
            x=data.get1(i)[0],
            y=data.get1(i)[1],
            text=data.get1(i)[2],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
            ) for i in tab],
        'layout': dict(
            xaxis={'type': 'log', 'title': 'Czas istnienia spółki [msc]'},
            yaxis={'title': 'Liczba unikalnych PKD'},
            # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }

