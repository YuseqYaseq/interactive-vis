# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
from dash import dependencies

external_stylesheets = ['https://raw.githubusercontent.com/plotly/dash-app-stylesheets/master/dash-analytics-report.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
exploration_div = html.Div(id='exploration_div', hidden=False)
model_div = html.Div(id='model_div', hidden=True)
app.layout = html.Div([
    html.Button('exploration', id='exploration_button', n_clicks=0),
    html.Button('model', id='model_button', n_clicks=0),
    exploration_div,
    model_div
])


@app.callback(
    [dependencies.Output('exploration_div', 'hidden'), dependencies.Output('model_div', 'hidden')],
    [dependencies.Input('exploration_button', 'n_clicks'), dependencies.Input('model_button', 'n_clicks')]
)
def update_page_exploration(e, m):
    ctx = dash.callback_context
    if not ctx.triggered or 'exploration_button' == ctx.triggered[0]['prop_id'].split('.')[0]:
        return [False, True]

    return [True, False]
