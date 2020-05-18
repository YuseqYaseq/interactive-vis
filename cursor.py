import pandas as pd
from math import isnan
import json

voivodeships = ['ŚWIĘTOKRZYSKIE', 'WIELKOPOLSKIE', 'KUJAWSKO-POMORSKIE', 'LUBELSKIE', 'ŚLĄSKIE',
                'MAŁOPOLSKIE', 'DOLNOŚLĄSKIE', 'LUBUSKIE', 'MAZOWIECKIE', 'OPOLSKIE', 'PODLASKIE',
                'POMORSKIE', 'PODKARPACKIE', 'ZACHODNIOPOMORSKIE', 'ŁÓDZKIE', 'WARMIŃSKO-MAZURSKIE']


def clean_voivodeships(x):
    if isinstance(x, str):
        x = x.upper()
        if x not in voivodeships:
            return float('nan')
        return x
    elif isnan(x):
        return x
    raise RuntimeError(f"Bad input {x}")


class Cursor:

    def __init__(self):
        self.df = pd.read_csv('data/ceidg_data_classif.csv', nrows=1000)
        self.df['MainAddressVoivodeship'] = self.df['MainAddressVoivodeship'].map(clean_voivodeships)

        with open('data/poland_geo.json', 'r', encoding='utf-8') as file:
            self.poland_map = json.load(file)
            for elem in self.poland_map['features']:
                elem['properties']['name'] = elem['properties']['name'].upper()

    def get1(self, target):
        return self.df[self.df['Target'] == target]['DurationOfExistenceInMonths'],\
               self.df[self.df['Target'] == target]['NoOfUniquePKDClasses'], \
               self.df[self.df['MainAddressVoivodeship'] == target]['RandomDate']

    def get2(self):
        return self.df.query("Sex=='M' and Target=='0'").count()['Target'],\
               self.df.query("Sex=='M' and Target=='1'").count()['Target'],\
               self.df.query("Sex=='F' and Target=='0'").count()['Target'],\
               self.df.query("Sex=='F' and Target=='1'").count()['Target']

    def get3(self):
        return self.df[['MainAndCorrespondenceAreTheSame']].groupby('MainAndCorrespondenceAreTheSame')['MainAndCorrespondenceAreTheSame'].count()

    def get4(self, month_value, voivod_value):
        month_filter = []
        voivod_filter = []
        for month in month_value:
            s = "MonthOfStartingOfTheBusiness == \"%s\"" % (month)
            month_filter.append(s)

        for voivod in voivod_value:
            s = "MainAddressVoivodeship == \"%s\"" % (voivod)
            voivod_filter.append(s)

        month_filter = " | ".join(month_filter)
        voivod_filter = " | ".join(voivod_filter)
        filtered_data = self.df.query(month_filter).query(voivod_filter)
        return filtered_data[['MainAndCorrespondenceAreTheSame']].groupby('MainAndCorrespondenceAreTheSame')['MainAndCorrespondenceAreTheSame'].count()

    def get_df(self):
        return self.df

    def get_target_per_voivodeship(self):
        ret = self.df.groupby(['MainAddressVoivodeship', 'Target']).size().unstack(fill_value=0)
        for voivodeship in voivodeships:
            if voivodeship not in list(ret.index):
                row = pd.Series({False: 0, True: 0}, name=voivodeship)
                ret = ret.append(row)
        ret['MainAddressVoivodeship'] = ret.index
        return ret

    def get_map(self):
        return self.poland_map


cursor = Cursor()


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('expand_frame_repr', False)
    classif = pd.read_csv('data/ceidg_data_classif.csv', nrows=1000)
    print(classif)
