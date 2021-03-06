import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

from app import app
from cursor import Cursor, cursor, voivodeships

bg_color = '#C2EABD'
font_settings = {'color': '#000000',
                 'size': 10}
continous_color_sequence = 'Fall'
discrete_color_sequence = ['#D4AA7D', '#967D69', '#92B9BD', '#272727']

html_elements = []

data = Cursor()

months, cont_by_month, discont_by_month = data.get_data_by_month()

values = cursor.get_target_by_month_and_voivod(None, ['LUBELSKIE'])

map_data_sex = cursor.get_target_per_category_voivodeship('Sex')
map_data_citizenship = cursor.get_target_per_category_voivodeship('HasPolishCitizenship')
map_data_shareholder = cursor.get_target_per_category_voivodeship('ShareholderInOtherCompanies')
map_data_updated_info = cursor.get_target_per_updated_info_voivodeship()
map_data_licence = cursor.get_target_per_category_voivodeship("HasLicences")


fig = px.choropleth_mapbox(cursor.get_target_per_voivodeship(),
                           geojson=cursor.get_map(),
                           locations='MainAddressVoivodeship', color=False,
                           featureidkey='properties.name',
                           color_continuous_scale=continous_color_sequence,
                           # range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=4.75, center={"lat": 52.11, "lon": 19.42},
                           opacity=0.5,
                           labels={'MainAddressVoivodeship': 'Województwo',
                                   'True': 'Zamknięte<br>przedsiębiorstwa',
                                   'False': 'Działające<br>przedsiębiorstwa'}
                           )

fig.update_layout(margin={"r": 0, "t": 0, "l": 30, "b": 0},
                  height=500,
                  width=600,
                  autosize=True,
                  clickmode='event+select',
                  plot_bgcolor=bg_color,
                  paper_bgcolor=bg_color)

html_elements.append(html.Div([
    # sex
    html.Div([
        html.H2('Dwuwartościowe cechy działalności a jej kontynuowanie',
                id='pie-charts',
                style={'float': 'left', 'width': '100%'}),
        dcc.Graph(id='map', figure=fig, style={'float': 'left', 'width': '40%', 'height': 650}),
        dcc.Graph(id='map_pie_sex', style={'float': 'left', 'width': '20%', 'height': 300}),
        dcc.Graph(id='map_pie_citizenship', style={'float': 'left', 'width': '20%', 'height': 300}),
        dcc.Graph(id='map_pie_shareholder', style={'float': 'left', 'width': '20%', 'height': 300}),
        dcc.Graph(id='map_pie_has_info', style={'float': 'left', 'width': '30%', 'height': 300}),
        dcc.Graph(id='map_pie_licence', style={'float': 'left', 'width': '30%', 'height': 300}),
        html.H2('Działalności kontynuowane i niekontynuowane w rozłożeniu na miesiące rozpoczęcia działalności',
                id='by-month',
                style={'float': 'left', 'width': '100%'}),
        dcc.Graph(id='business_by_month', style={'float': 'left', 'width': '100%', 'height': 400}),
        html.H2('Procent firm, które wstrzymają działalność w zależności od posiadanej ilości sekcji PKD',
                id='by-sectionCount',
                style={'float': 'left', 'width': '100%'}),
        dcc.Graph(id='terminated_by_sections', style={'float': 'left', 'width': '100%', 'height': 400}),
        html.H2('Procent firm, które wstrzymają działalność w zależności od nazw sekcji PKD',
                id='by-sectionName',
                style={'float': 'left', 'width': '100%'}),
        dcc.Graph(id='terminated_by_sectionName', style={'float': 'left', 'width': '100%', 'height': 600}),
        html.H2('Procent firm, które wstrzymają działalność w zależności od posiadanej ilości klas PKD',
                id='by-classesCount',
                style={'float': 'left', 'width': '100%'}),
        dcc.Graph(id='terminated_by_classes', style={'float': 'left', 'width': '100%', 'height': 400}),
    ])]))


def get_map_piechart_fig(selectedData, map_data, pie_names, title):
    if selectedData is None:
        selected_voivodeships = voivodeships
    else:
        selected_voivodeships = [elem['location'] for elem in selectedData['points']]
    values = map_data[map_data['MainAddressVoivodeship'].isin(selected_voivodeships)]
    values = [values[column].sum() for column in map_data.columns[:-1]]
    names = [pie_names[column] for column in map_data.columns[:-1]]
    fig = px.pie(names=names, values=values, title=title, color_discrete_sequence=discrete_color_sequence)
    fig.update_layout(margin={"r": 50, "t": 50, "l": 50, "b": 50},
                      height=300,
                      plot_bgcolor=bg_color,
                      paper_bgcolor=bg_color,
                      font=font_settings)
    return fig


def get_business_by_month_barchart_fig(selected_data):
    if selected_data is None:
        selected_voivodeships = voivodeships
    else:
        selected_voivodeships = [elem['location'] for elem in selected_data['points']]
    values = cursor.get_target_by_month_and_voivod(None, selected_voivodeships)
    fig = go.Figure(data=[
        go.Bar(name='Kontynuowane', x=values[0].index.values, y=values[0].values,
               marker_color=discrete_color_sequence[0]),
        go.Bar(name='Niekontynuowane', x=values[1].index.values, y=values[1].values,
               marker_color=discrete_color_sequence[1])
    ])
    fig.update_layout(margin={"r": 50, "t": 50, "l": 50, "b": 50},
                      height=300,
                      plot_bgcolor=bg_color,
                      paper_bgcolor=bg_color,
                      font=font_settings, )

    return fig

def get_terminated_byNumberOfUniqueSections_barchart_fig(selected_data):
    if selected_data is None:
        selected_voivodeships = voivodeships
    else:
        selected_voivodeships = [elem['location'] for elem in selected_data['points']]
    
    values = cursor.get_terminated_byNumberOfUniqueSections(selected_voivodeships)
    fig = go.Figure(data=[
        go.Bar(name='Procent firm, które wstrzymają działalność', x=values.index.values, y=values, marker_color=discrete_color_sequence[0]),
    ])
    fig.update_layout(margin={"r": 50, "t": 50, "l": 50, "b": 50},
                      height=300,
                      plot_bgcolor=bg_color,
                      paper_bgcolor=bg_color,
                      font=font_settings,)

    return fig

def get_terminated_bySectionName_barchart_fig(selected_data):
    if selected_data is None:
        selected_voivodeships = voivodeships
    else:
        selected_voivodeships = [elem['location'] for elem in selected_data['points']]

    values = cursor.get_terminated_bySectionName(selected_voivodeships)
    fig = go.Figure(data=[
        go.Bar(name='Procent firm, które wstrzymają działalność', x=values.index.values, y=values, marker_color=discrete_color_sequence[0]),
    ])
    fig.update_layout(margin={"r": 50, "t": 50, "l": 50, "b": 50},
                      height=300,
                      plot_bgcolor=bg_color,
                      paper_bgcolor=bg_color,
                      font=font_settings,)

    return fig

def get_terminated_byNumberOfUniqueClasses_scatter_fig(selected_data):
    if selected_data is None:
        selected_voivodeships = voivodeships
    else:
        selected_voivodeships = [elem['location'] for elem in selected_data['points']]
    
    values = cursor.get_terminated_byNumberOfUniqueClasses(selected_voivodeships)
    fig = px.scatter(values, y="NoOfUniquePKDClasses", x=values.index, color_discrete_sequence=discrete_color_sequence)
    fig.update_layout(margin={"r": 50, "t": 50, "l": 50, "b": 50},
                      height=300,
                      plot_bgcolor=bg_color,
                      paper_bgcolor=bg_color,
                      font=font_settings)
    fig.update_traces(marker=dict(size=12, line=dict(width=3)),
                                               selector=dict(mode='markers'))
    fig.update_xaxes(title_text='Liczba unikatowych klas PKD')
    fig.update_yaxes(title_text='Procent firm, które wstrzymają działalność')
    return fig


@app.callback(
    [Output('map_pie_sex', 'figure'),
     Output('map_pie_citizenship', 'figure'),
     Output('map_pie_shareholder', 'figure'),
     Output('map_pie_licence', 'figure'),
     Output('map_pie_has_info', 'figure'),
     Output('business_by_month', 'figure'),
     Output('terminated_by_sections', 'figure'),
     Output('terminated_by_classes', 'figure'),
     Output('terminated_by_sectionName', 'figure')],
    [Input('map', 'selectedData')])
def display_selected_data(selectedData):
    return get_map_piechart_fig(selectedData,
                                map_data_sex,
                                {'False_F': 'Kobieta, 0',
                                 'False_M': 'Mężczyzna, 0',
                                 'True_F': 'Kobieta, 1',
                                 'True_M': 'Mężczyzna, 1'},
                                'Odsetek kobiet i mężczyzn'), \
           get_map_piechart_fig(selectedData,
                                map_data_citizenship,
                                {'True_True': 'Polak, 1',
                                 'False_True': 'Polak, 0',
                                 'True_False': 'Obcokrajowiec, 1',
                                 'False_False': 'Obcokrajowiec, 0'},
                                'Odsetek Polaków i obcokrajowców'), \
           get_map_piechart_fig(selectedData,
                                map_data_shareholder,
                                {'True_True': 'Udziałowiec, 1',
                                 'True_False': 'Nieudziałowiec, 1',
                                 'False_True': 'Udziałowiec, 0',
                                 'False_False': 'Nieudziałowiec, 0'},
                                'Odsetek udziałowców w innych przedsiębiorstwach'), \
           get_map_piechart_fig(selectedData,
                                map_data_licence,
                                {'True_True': 'Posiada licencję, 1',
                                 'True_False': 'Nie posiada licencji, 1',
                                 'False_True': 'Posiada licencję, 0',
                                 'False_False': 'Nie posiada licencji, 0'},
                                ' Odsetek firm posiadających licencję'), \
           get_map_piechart_fig(selectedData,
                                map_data_updated_info,
                                {'True_HasInfo': 'Wypełnione dane, 1',
                                 'False_HasInfo': 'Wypełnione dane, 0',
                                 'True_NoInfo': 'Niewypełnione dane, 1',
                                 'False_NoInfo': 'Niewypełnione dane, 0'},
                                'Odsetek przedsiębiorstw z wypełnionymi danymi kontaktowymi'), \
           get_business_by_month_barchart_fig(selectedData), \
           get_terminated_byNumberOfUniqueSections_barchart_fig(selectedData), \
           get_terminated_byNumberOfUniqueClasses_scatter_fig(selectedData), \
           get_terminated_bySectionName_barchart_fig(selectedData)
