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

    def get_target_per_category_voivodeship(self, category_name):
        ret = self.df.groupby(['MainAddressVoivodeship', category_name, 'Target'])\
            .size().unstack(fill_value=0).unstack(fill_value=0)
        ret.columns = [str(i[0]) + '_' + str(i[1]) for i in list(ret.columns)]
        for row in self.__yield_rows_for_missing_voivodeships(list(ret.index),
                                                              dict(zip(ret.columns, [0 for _ in ret.columns]))):
            ret = ret.append(row)
        ret['MainAddressVoivodeship'] = ret.index
        return ret

    def get_target_per_updated_info_voivodeship(self):
        ret = self.df.query('IsPhoneNo == True and IsEmail == True and IsWWW == True')\
                     .groupby(['MainAddressVoivodeship', 'Target'])\
                     .size().unstack(fill_value=0)
        for row in self.__yield_rows_for_missing_voivodeships(list(ret.index), {False: 0, True: 0}):
            ret = ret.append(row)
        ret2 = self.df.query('IsPhoneNo == False or IsEmail == False or IsWWW == False') \
            .groupby(['MainAddressVoivodeship', 'Target']) \
            .size().unstack(fill_value=0)
        for row in self.__yield_rows_for_missing_voivodeships(list(ret2.index), {False: 0, True: 0}):
            ret2 = ret2.append(row)
        ret.columns = [str(i) + '_HasInfo' for i in list(ret.columns)]
        ret2.columns = [str(i) + '_NoInfo' for i in list(ret2.columns)]
        ret = ret.join(ret2)
        ret['MainAddressVoivodeship'] = ret.index
        return ret

    def get_df(self):
        return self.df

    def get_target_per_voivodeship(self):
        ret = self.df.groupby(['MainAddressVoivodeship', 'Target']).size().unstack(fill_value=0)
        for row in self.__yield_rows_for_missing_voivodeships(list(ret.index), {False: 0, True: 0}):
            ret = ret.append(row)
        ret['MainAddressVoivodeship'] = ret.index
        return ret

    def group_by_county(self):
        return self.df.groupby(['MainAddressVoivodeship', 'MainAddressCounty']).size().unstack(fill_value=0)

    def get_map(self):
        return self.poland_map

    @staticmethod
    def __yield_rows_for_missing_voivodeships(current_list, fill_dict):
        for voivodeship in voivodeships:
            if voivodeship not in current_list:
                yield pd.Series(fill_dict, name=voivodeship)


cursor = Cursor()


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('expand_frame_repr', False)
    classif = pd.read_csv('data/ceidg_data_classif.csv', nrows=1000)
    print(classif)
