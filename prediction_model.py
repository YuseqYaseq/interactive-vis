import json

import dash
import dash_html_components as html
import dash_core_components as dcc
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Output, Input

from net import get_statistics
from app import app
from cursor import cursor

html_elements = []


def create_table(array):
    return html.Table([html.Tr([html.Th([array[i, j]]) for j in range(array.shape[1])]) for i in range(array.shape[0])])


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

map_data = cursor.get_target_per_sex_voivodeship()

def add():
    # confusion matrix
    data, x_test, pred_y, output, y_test, cm = get_statistics()
    cm = [['', 'Predicted False', 'Predicted True'],
          ['Actual False', cm[0][0], cm[0][1]],
          ['Actual True', cm[1][0], cm[1][1]]]
    params_dropdown = [{'label': c, 'value': c} for c in ['1', '2']]
    html_elements.append(create_table(np.array(cm)))
    html_elements.append(dcc.Dropdown(id='scatter_dropdown',
                                      options=params_dropdown,
                                      value='1'))
    html_elements.append(html.Div(dcc.Graph(figure=get_scatter_figure(data,
                                                                      'NoOfUniquePKDDivsions',
                                                                      'NoOfUniquePKDClasses',),
                                            style={'height': 450}),
                                  id='scatter1'))

    html_elements.append(html.Div(dcc.Graph(figure=get_scatter_figure(data,
                                                                      'PKDMainDivision',
                                                                      'NoOfUniquePKDClasses', ),
                                            style={'height': 450}),
                                  id='scatter2',
                                  hidden=True))

    pred_error = get_pred_error(output, y_test)
    pred_error.sort(reverse=True)
    html_elements.append(html.Div(dcc.Graph(id='bar1',
                                            figure=px.bar(x=[i for i, _ in enumerate(pred_error)],
                                                          y=pred_error,
                                                          hover_name=['temp_name' for i, _ in enumerate(pred_error)]),
                                            style={'height': 450})))

    fig = px.choropleth_mapbox(cursor.get_target_per_voivodeship(),
                               geojson=cursor.get_map(),
                               locations='MainAddressVoivodeship', color=True,
                               featureidkey='properties.name',
                               color_continuous_scale="Viridis",
                               # range_color=(0, 12),
                               mapbox_style="carto-positron",
                               zoom=5.5, center={"lat": 52.11, "lon": 19.42},
                               opacity=0.5,
                               labels={'MainAddressVoivodeship': 'Województwo',
                                       'True': 'Działające przedsiębiorstwa',
                                       'False': 'Zamknięte przedsiębiorstwa'}
                               )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      height=700,
                      width=1000,
                      autosize=True,
                      clickmode='event+select')

    ############
    html_elements.append(html.Div([
        html.Div([
            html.Div([
                dcc.Graph(id='map', figure=fig)
            ], style={'float': 'left','margin': 'auto'}),
            html.Div([
                dcc.Graph(figure=px.pie(names=['m, 1', 'm, 0', 'f, 1', 'f, 0'],
                                        values=cursor.get_target_per_sex()),
                          id='map_pie',
                          style={'height': 700, 'width': 550}),
                html.P("ABC")
            ], style={'float': 'right', 'margin': 'auto'})
        ])]))


@app.callback(
    Output('map_pie', 'figure'),
    [Input('map', 'selectedData')])
def display_selected_data(selectedData):

    if selectedData is None:
        values = cursor.get_target_per_sex()
    else:
        selected_voivodeships = [elem['location'] for elem in selectedData['points']]
        values = map_data[map_data['MainAddressVoivodeship'].isin(selected_voivodeships)]
        values = [values[column].sum() for column in ['False_M', 'True_M', 'False_F', 'True_F']]
    fig=px.pie(names=['m, 0', 'm, 1', 'f, 0', 'f, 1'], values=values)
    return fig

#########

@app.callback(
    [Output('scatter1', 'hidden'), Output('scatter2', 'hidden')],
    [Input('scatter_dropdown', 'value')]
)
def update_covid_graph(dropdown_value):
    ctx = dash.callback_context
    if not ctx.triggered or dropdown_value == '1':
        return [False, True]

    return [True, False]


add()
