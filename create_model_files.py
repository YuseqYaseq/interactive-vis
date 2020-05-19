#!/usr/bin/python3
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from lightgbm import LGBMClassifier
from joblib import dump
import os

from utils import evaluate

SAMPLE = False
RANDOM_SEED = 1
np.random.seed(RANDOM_SEED)


def create_lgbm(data):
    """Creates files used in application (transformed dataframes and model)."""

    categorical_variables = [
        "MonthOfStartingOfTheBusiness",
        "MainAddressVoivodeship",
        "CorrespondenceAddressVoivodeship",
        "CorrespondenceAddressCounty",
        "PKDMainSection",
        "Sex",
        "MainAddressCounty",
        "CommunityProperty"
    ]
    for col in categorical_variables:
        data[col] = data[col].astype('category')

    x_train, x_test, y_train, y_test = train_test_split(data.drop(["Target", "RandomDate"], axis=1), data["Target"],
                                                        random_state=RANDOM_SEED)
    # Creating, fitting and saving LGBM classifier
    print("Fitting LGBM Classifier...")
    clf = LGBMClassifier(n_estimators=100)
    clf.fit(x_train, y_train)
    print("Done")
    dump(clf, "models/lgbm.joblib")

    # Adding predictions to dataframe and saving to file
    predicted_target = clf.predict(x_test)
    predicted_proba = clf.predict_proba(x_test)[:, 1]
    x_test["PredictedTarget"] = predicted_target
    x_test["PredictedProba"] = predicted_proba
    x_test["Target"] = y_test
    x_test.to_csv("models/x_test_lgbm.csv", index=False)
    print("Saved LGBM classifier and dataframe")

def create_lr(data):
    x_train, x_test, y_train, y_test = train_test_split(data.drop("Target", axis=1), data["Target"],
                                                        random_state=RANDOM_SEED)
    # Creating variable processing pipeline
    categorical_variables = ["MonthOfStartingOfTheBusiness", "MainAddressVoivodeship", "PKDMainSection", "Sex"]
    numerical_variables = [
        "MainAndCorrespondenceAreTheSame",
        "DurationOfExistenceInMonths",
        "NoOfAdditionalPlaceOfTheBusiness",
        "IsPhoneNo",
        "IsEmail",
        "IsWWW",
        "NoOfLicences",
        "HasPolishCitizenship",
        "ShareholderInOtherCompanies"
    ]

    impute_encode = Pipeline([
        ("impute", SimpleImputer(strategy="constant", fill_value="unknown")),
        ("one_hot_enocde", OneHotEncoder(handle_unknown="ignore"))
    ])

    scale = Pipeline([
        ("min_max_scale", MinMaxScaler())
    ])

    column_transformer = ColumnTransformer([
        ("one_hot_encoder", impute_encode, categorical_variables),
        ("numerical_variables", scale, numerical_variables)
    ])

    # Creating, fitting and saving Logistic Regression classifier
    pipeline = Pipeline([
        ("get_features", column_transformer),
        ("classifier", LogisticRegression(max_iter=1000, tol=1e-4, C=100, solver="saga", n_jobs=4))
    ])
    print("Fitting logistic regression classifier (may take a while)...")
    pipeline.fit(x_train, y_train)
    print("Done")

    dump(pipeline, "models/lr.joblib")

    # Adding predictions to dataframe and saving
    predicted_target = pipeline.predict(x_test)
    predicted_proba = pipeline.predict_proba(x_test)[:, 1]
    x_test["PredictedTarget"] = predicted_target
    x_test["PredictedProba"] = predicted_proba
    x_test["Target"] = y_test
    x_test.to_csv("models/x_test_lr.csv", index=False)
    print("Saved logistic regression classifier and dataframe")


if __name__ == "__main__":
    model_dir = "models"
    if not os.path.exists(model_dir):
        os.mkdir(model_dir)
    print("Reading data...")
    data = pd.read_csv("data/ceidg_data_classif.csv")
    print("Done")
    if SAMPLE:
        data = data.sample(SAMPLE)
    create_lgbm(data)
    create_lr(data)
