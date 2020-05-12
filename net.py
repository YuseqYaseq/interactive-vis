import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras import Sequential
from keras.layers import Dense, Dropout
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.metrics import confusion_matrix

from cursor import cursor


class DenseTransformer(BaseEstimator, TransformerMixin):

    def transform(self, x):
        return x.toarray()
        #return x

    def fit(self, x, y=None, **fit_params):
        return self


def create_model():
    model = Sequential()
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(2, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer="Adam", metrics=['accuracy'])
    return model


def build_pipeline():
    categorical_variables = ["MonthOfStartingOfTheBusiness", "MainAddressVoivodeship", "PKDMainSection", "Sex"]
    numerical_variables = [
        "MainAndCorrespondenceAreTheSame",
        "DurationOfExistenceInMonths",
        "NoOfAdditionalPlaceOfTheBusiness",
        "IsPhoneNo",
        "IsEmail",
        "IsWWW",
        # "HasLicences",  # useless since we have NoOfLicenses
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

    pipeline = Pipeline([
        ("get_features", column_transformer),
        ("dense_transformer", DenseTransformer()),
        ("classifier", KerasRegressor(build_fn=create_model,
                                      verbose=1,
                                      epochs=2,
                                      class_weight={0: 86, 1: 14}))
    ])
    return pipeline


def get_statistics():
    RANDOM_SEED = 42
    np.random.seed(RANDOM_SEED)
    data = cursor.get_df()

    x_train, x_test, y_train, y_test = train_test_split(data.drop("Target", axis=1), data["Target"],
                                                        random_state=RANDOM_SEED)

    y_train = np.array(y_train, dtype=float)
    y_test = np.array(y_test, dtype=float)
    pipeline = build_pipeline()
    pipeline.fit(x_train, y_train)
    output = pipeline.predict(x_test)
    pred_y = np.argmax(output, axis=1)

    cm = confusion_matrix(pred_y, y_test)
    return data, x_test, pred_y, output, y_test, cm


if __name__ == '__main__':
    print(get_statistics())