# coding=utf-8

import dash_html_components as html
import dash_core_components as dcc
from dash import dependencies
import plotly.express as px
import plotly.graph_objects as go

from app import app
from cursor import Cursor

html_elements = []

counter = 0
data = Cursor()
fig1 = px.pie(names=['m, 0', 'm, 1', 'f, 0', 'f, 1'], values=data.get2())
barchart = px.bar(
    x=['NIE', 'TAK'],
    y=data.get4(['January', 'February', 'March', 'April', 'June', 'July'], ['MAZOWIECKIE']),
    title='Czy działalność kontynuowano nieprzerwanie przez okres 12 miesięcy?'
)

months, cont_by_month, discont_by_month = data.get_data_by_month()

barchart_by_month = go.Figure(data=[
    go.Bar(name='Kontynuowane', x=months, y=cont_by_month),
    go.Bar(name='Niekontynuowane', x=months, y=discont_by_month)
])

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
    dcc.Graph(figure=fig1),
    dcc.Dropdown(
        id='month-dropdown',
        options=[
            {'label': 'Styczeń', 'value': 'January'},
            {'label': 'Luty', 'value': 'February'},
            {'label': 'Marzec', 'value': 'March'},
            {'label': 'Kwiecień', 'value': 'April'},
            {'label': 'Maj', 'value': 'May'},
            {'label': 'Czerwiec', 'value': 'June'},
            {'label': 'Lipiec', 'value': 'July'},
            {'label': 'Sierpień', 'value': 'August'},
            {'label': 'Wrzesień', 'value': 'September'},
            {'label': 'Październik', 'value': 'October'},
            {'label': 'Listopad', 'value': 'November'},
            {'label': 'Grudzień', 'value': 'December'}
        ],
        value=['January', 'February', 'March', 'April', 'June', 'July'],
        multi=True
    ),
    dcc.Dropdown(
        id='voivodeship-dropdown',
        options=[
            {'label': 'dolnośląskie', 'value': 'DOLNOŚLĄSKIE'},
            {'label': 'kujawsko-pomorskie', 'value': 'KUJAWSKO-POMORSKIE'},
            {'label': 'lubelskie', 'value': 'LUBELSKIE'},
            {'label': 'lubuskie', 'value': 'LUBUSKIE'},
            {'label': 'łódzkie', 'value': 'ŁÓDZKIE'},
            {'label': 'małopolskie', 'value': 'MAŁOPOLSKIE'},
            {'label': 'mazowieckie', 'value': 'MAZOWIECKIE'},
            {'label': 'opolskie', 'value': 'OPOLSKIE'},
            {'label': 'podkarpackie', 'value': 'PODKARPACKIE'},
            {'label': 'podlaskie', 'value': 'PODLASKIE'},
            {'label': 'pomorskie', 'value': 'POMORSKIE'},
            {'label': 'śląskie', 'value': 'ŚLĄSKIE'},
            {'label': 'świętokrzyskie', 'value': 'ŚWIĘTOKRZYSKIE'},
            {'label': 'warmińsko-mazurskie', 'value': 'WARMIŃSKO-MAZURSKIE'},
            {'label': 'wielkopolskie', 'value': 'WIELKOPOLSKIE'},
            {'label': 'zachodniopomorskie', 'value': 'ZACHODNIOPOMORSKIE'},
        ],
        value=['MAZOWIECKIE'],
        multi=True
    ),
    html.Ul([
        html.Li("aaa"),
        html.Li("bbb")
    ]),
    dcc.Graph(
        id='graph2',
        figure=barchart
    ),
    html.Div([
        html.Table([
            html.Tr([
                html.Td(id='output', children=html.Span("Tutaj jakiś tekst")),
                html.Td(
                    rowSpan=3,
                    children=dcc.Graph(
                        id='graph3',
                        figure=barchart_by_month
                    )
                )
            ]),
            html.Tr(html.Td(html.Span("Tutaj jakiś tekst"))),
            html.Tr(html.Td(html.Span("Tutaj jakiś tekst")))
        ]),
        # dcc.Graph(
        #     id='graph3',
        #     figure=barchart_by_month
        # )
    ])
], ))


@app.callback(
    dependencies.Output('output', 'children'),
    [dependencies.Input('graph3', 'selectedData')]
)
def event_cb(event_data):
    print(event_data)
    counter = counter + 1
    return html.Span(f"Tutaj jakiś tekst: {counter}")


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


@app.callback(
    dependencies.Output('graph2', 'figure'),
    [
        dependencies.Input('month-dropdown', 'value'),
        dependencies.Input('voivodeship-dropdown', 'value')
    ]
)
def update_barchart(month_value, voivod_value):
    new_barchart = px.bar(
        x=['NIE', 'TAK'],
        y=data.get4(month_value, voivod_value),
        title='Czy działalność kontynuowano nieprzerwanie przez okres 12 miesięcy?'
    )
    return new_barchart
