import dash_html_components as html
import dash_core_components as dcc
from dash import dependencies
import plotly.express as px
import plotly.graph_objects as go

from app import app
from cursor import Cursor, cursor

html_elements = []

data = Cursor()

months, cont_by_month, discont_by_month = data.get_data_by_month()

values = cursor.get_target_by_month_and_voivod(None, ['LUBELSKIE'])
fig = go.Figure(data=[
    go.Bar(name='Kontynuowane', x=values[0].index.values, y=values[0].values),
    go.Bar(name='Niekontynuowane', x=values[1].index.values, y=values[1].values)
])

mostTerminatedData = data.get_mostTerminated()
mostTerminatedFigure = go.Figure(data=[
    go.Bar(x=mostTerminatedData.index.values, y=mostTerminatedData.values)
])

terminatedByUniqueClassesData = data.get_terminated_byNumberOfUniqueClasses()
terminatedByUniqueClassesFigure = px.scatter(terminatedByUniqueClassesData, y="NoOfUniquePKDClasses", x=terminatedByUniqueClassesData.index)
terminatedByUniqueClassesFigure.update_traces(marker=dict(size=12, line=dict(width=3)),
                                               selector=dict(mode='markers'))

terminatedByUniqueSectionsData = data.get_terminated_byNumberOfUniqueSections()
terminatedByUniqueSectionsFigure = px.scatter(terminatedByUniqueSectionsData, y="NoOfUniquePKDSections", x=terminatedByUniqueSectionsData.index)
terminatedByUniqueSectionsFigure.update_traces(marker=dict(size=12, line=dict(width=3)),
                                               selector=dict(mode='markers'))

terminatedByLicensePossesionRatioData = data.get_terminated_byLicensePossesionRatio()
terminatedByLicensePossesionRatioFigure = go.Figure(data=[
    go.Bar(x=terminatedByLicensePossesionRatioData.index.values, y=terminatedByLicensePossesionRatioData.values)
])

terminatedByLicensePossesionAllData = data.get_terminated_byLicensePossesionAll()
terminatedByLicensePossesionAllFigure = px.pie(names=terminatedByLicensePossesionAllData.index.values, values=terminatedByLicensePossesionAllData.values)

terminatedByDurationOfExistenceData = data.get_terminated_byDurationOfExistence()
terminatedByDurationOfExistenceFigure = go.Figure(data=[
    go.Scatter(x=terminatedByDurationOfExistenceData.index.values, y=terminatedByDurationOfExistenceData.values)
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
    dcc.Graph(
        id='graph3',
        figure=fig
    ),
    html.H3("Sekcje, gdzie najrzadziej kontynuują działalność w okresie 12 miesięcy"),
    dcc.Graph(
        id='mostTerminatedGraph',
        figure = mostTerminatedFigure,
    ),
    html.H3("Procent firm które wstrzymały swoją działalność w zależności od liczby unikalnych klas PKD"),
    dcc.Graph(
        id='mostTerminatedByUniqueClasses',
        figure = terminatedByUniqueClassesFigure,
    ),
    html.H3("Procent firm które wstrzymały swoją działalność w zależności od liczby unikalnych sekcji PKD"),
    dcc.Graph(
        id='mostTerminatedByUniqueSections',
        figure = terminatedByUniqueSectionsFigure,
    ),
    html.H3("Jaki procent firm które posiadają/nie posiadają licencji zawiesza działalność w okresie 12 miesięcy"),
    dcc.Graph(
        id='terminatedByLicensePossesionRatio',
        figure=terminatedByLicensePossesionRatioFigure
    ),
    html.H3("Jaki procent wśród firm, które zawiesza działalność w okresie 12 miesięcy stanowią firmy z licencją/bez licencji"),
    dcc.Graph(
        id='terminatedByLicensePossesionAll',
        figure=terminatedByLicensePossesionAllFigure
    ),
    html.H3("Jaki procent firm zamknie swoją działalność w okresie 12 miesięcy w zależności od ilości miesięcy życia firmy"),
    dcc.Graph(
        id='terminatedByDurationOfExistence',
        figure=terminatedByDurationOfExistenceFigure
    ),
], ))


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

