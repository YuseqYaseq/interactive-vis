import dash
import dash_html_components as html
import dash_core_components as dcc
from dash import dependencies
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

from app import app
from cursor import cursor, voivodeships

interactive_statistics_html = []

df = pd.read_csv("data/ceidg_data_classif.csv")

barplot_div = html.Div([
    dcc.Graph(id="statistics-graph"),
])

layout = html.Div([
    html.Div(
        dcc.Markdown(
            """
            #### Check a category
            """
        )
    ),
    dcc.RadioItems(
        id="sex-option",
        options=[
            dict(label="Man", value="M"),
            dict(label="Woman", value="F")
        ],
        value="M"
    ),
    dcc.RadioItems(
        id="voivodeship-option",
        options=[
            dict(label=v, value=v) for v in voivodeships
        ],
        value=voivodeships[0]
    ),
    html.Div(id="number-of-observations"),
    barplot_div
])


@app.callback(
    [
        dependencies.Output("statistics-graph", "figure"), # figure is the output property of a statistics-graph
        dependencies.Output("number-of-observations", "children")
    ],
    [
        dependencies.Input("sex-option", "value"),
        dependencies.Input("voivodeship-option", "value")
    ]
)
def update_barplot(selected_sex, selected_voivodeship):
    failed, n = cursor.get_subset_summary(Sex=selected_sex, MainAddressVoivodeship=selected_voivodeship)
    fig = {
        "data": [
            {
                "x": ["failed", "not failed"],
                "y": [failed, 1 - failed],
                "type": "bar",

            }
        ],
        "layout": {
            "title": 'Percentage of failed companies per selected category',
            "yaxis": dict(type="bar", range=[0, 1])
        }
    }
    number_of_observations_text = "Number of observations with selected values: {}".format(n)
    return fig, number_of_observations_text


interactive_statistics_html.append(layout)

terminated_idx = df["Target"] == 1

categorical_variables = [
    "MonthOfStartingOfTheBusiness",
    "MainAddressVoivodeship",
    "CorrespondenceAddressVoivodeship",
    # "CorrespondenceAddressCounty",
    "PKDMainSection",
    "Sex",
    "MainAddressCounty",
    "CommunityProperty"
]

# fig = px.bar(df, x="sex", y="total_bill", color="smoker", barmode="group",
#              facet_row="time", facet_col="day",
#              category_orders={"day": ["Thur", "Fri", "Sat", "Sun"],
#                               "time": ["Lunch", "Dinner"]})
# fig.show()
