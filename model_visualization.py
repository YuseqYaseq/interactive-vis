import dash
import dash_html_components as html
import dash_core_components as dcc
from dash import dependencies
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import joblib
from sklearn.metrics import precision_recall_curve, roc_curve

from app import app
from cursor import cursor, voivodeships


lr = joblib.load("models/lr.joblib")
lgbm = joblib.load("models/lgbm.joblib")
x_lgbm = pd.read_csv("models/x_test_lgbm.csv")
x_lr = pd.read_csv("models/x_test_lr.csv")

model_visualization_html = []

barplot_div = html.Div([
    dcc.Graph(id="statistics-graph"),
])


def get_precision_recall_figure(model_name):
    assert model_name in ("lgbm", "lr")
    x = x_lr if model_name == "lr" else x_lgbm
    pr_curve = precision_recall_curve(x["Target"], x["PredictedProba"])
    return dict(
        data=[
            {
                "x": pr_curve[1],  # 1 is first because we want recall as x axis (not precision)
                "y": pr_curve[0],
            }
        ],
        layout={
            "xaxis": dict(title="recall"),
            "yaxis": dict(title="precision")
        }
    )


def get_roc_figure(model_name):
    assert model_name in ("lgbm", "lr")
    x = x_lr if model_name == "lr" else x_lgbm
    curve = roc_curve(x["Target"], x["PredictedProba"])
    return dict(
        data=[
            {
                "x": curve[0],
                "y": curve[1],
            }
        ],
        layout={
            "xaxis": dict(title="False Positive Rate"),
            "yaxis": dict(title="True Positive Rate")
        }
    )


@app.callback(
    dependencies.Output("lr-feature-importance", "figure"),
    [dependencies.Input("lr-importance-slider", "value")]
)
def update_lr_importance(n_features):
    def get_transformer_feature_names(column_transformer):
        """Most important features from a pipeline."""
        output_features = []
        for name, pipe, features in column_transformer.transformers_:
            if name != 'remainder':
                for i in pipe:
                    trans_features = []
                    if hasattr(i, 'categories_'):
                        trans_features.extend(i.get_feature_names(features))
                    else:
                        trans_features = features
                output_features.extend(trans_features)
        return output_features
    feature_names = get_transformer_feature_names(lr["get_features"]);
    feature_scores = lr["classifier"].coef_[0]
    name_score = list(zip(feature_names, feature_scores))
    name_score.sort(key=lambda t: abs(t[1]), reverse=True)
    top_name_scores = name_score[:n_features]
    top_names, top_scores = zip(*top_name_scores)
    fig = {
        "data": [
            {
                "x": top_names,
                "y": top_scores,
                "type": "bar",

            }
        ],
        "layout": {
            "title": 'Feature importance (coefficients) for logistic regression'
        }
    }
    return fig


@app.callback(
    dependencies.Output("lgbm-feature-importance", "figure"),
    [dependencies.Input("lgbm-importance-slider", "value")]
)
def update_lr_importance(n_features):
    feature_names = ['MonthOfStartingOfTheBusiness', 'QuarterOfStartingOfTheBusiness',
                     'MainAddressVoivodeship', 'MainAddressCounty', 'MainAddressTERC',
                     'CorrespondenceAddressVoivodeship', 'CorrespondenceAddressCounty',
                     'CorrespondenceAddressTERC', 'MainAndCorrespondenceAreTheSame',
                     'DurationOfExistenceInMonths', 'NoOfAdditionalPlaceOfTheBusiness',
                     'IsPhoneNo', 'IsEmail', 'IsWWW', 'CommunityProperty', 'HasLicences',
                     'NoOfLicences', 'Sex', 'HasPolishCitizenship',
                     'ShareholderInOtherCompanies', 'PKDMainSection', 'PKDMainDivision',
                     'PKDMainGroup', 'PKDMainClass', 'NoOfUniquePKDSections',
                     'NoOfUniquePKDDivsions', 'NoOfUniquePKDGroups', 'NoOfUniquePKDClasses']

    feature_scores = lgbm.feature_importances_
    name_score = list(zip(feature_names, feature_scores))
    name_score.sort(key=lambda t: abs(t[1]), reverse=True)
    top_name_scores = name_score[:n_features]
    top_names, top_scores = zip(*top_name_scores)
    fig = {
        "data": [
            {
                "x": top_names,
                "y": top_scores,
                "type": "bar",

            }
        ],
        "layout": {
            "title": 'Feature importance (number of splits) for lgbm classfier'
        }
    }
    return fig


lr_tab = html.Div([
    html.H2("Regresja logistyczna"),
    html.Div([
        html.Div([
            html.H3("Krzywa Precision-Recall"),
            dcc.Graph(figure=get_precision_recall_figure("lr")),
        ], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.H3("Krzywa ROC"),
            dcc.Graph(figure=get_roc_figure("lr"))
        ], style={'width': '49%', 'display': 'inline-block'})
    ]),
    html.Div([
        html.H3("Znaczenie cech"),
        dcc.Slider(id="lr-importance-slider", min=3, max=69, step=1, value=10, tooltip=dict(always_visible=True)),
        html.H5("Number of most important features"),
        dcc.Graph(id="lr-feature-importance")
    ])
])

lgbm_tab = html.Div([
    html.H2("Klasyfikator LGBM"),
    html.Div([
        html.Div([
            html.H3("Krzywa Precision-Recall"),
            dcc.Graph(figure=get_precision_recall_figure("lgbm")),
        ], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.H3("Krzywa ROC"),
            dcc.Graph(figure=get_roc_figure("lgbm"))
        ], style={'width': '49%', 'display': 'inline-block'})
    ]),
    html.Div([
        html.H3("Znaczenie cech"),
        dcc.Slider(id="lgbm-importance-slider", min=3, max=28, step=1, value=10, tooltip=dict(always_visible=True)),
        html.H5("Liczba wyświetlanych najważniejszych cech"),
        dcc.Graph(id="lgbm-feature-importance")
    ])
])

layout = html.Div([
    html.H1("Porównanie modeli klasyfikujących"),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Regresja logistyczna', value='lr', children=[lr_tab]),
        dcc.Tab(label='Klasyfikator LGBM', value='lgbm', children=[lgbm_tab]),
    ]),
    html.Div(id='tabs-content')
], style={'float': 'left', 'width': '100%'})

model_visualization_html.append(layout)
