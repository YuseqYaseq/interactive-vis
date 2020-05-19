import pandas as pd
from math import isnan
import json

voivodeships = ['ŚWIĘTOKRZYSKIE', 'WIELKOPOLSKIE', 'KUJAWSKO-POMORSKIE', 'LUBELSKIE', 'ŚLĄSKIE',
                'MAŁOPOLSKIE', 'DOLNOŚLĄSKIE', 'LUBUSKIE', 'MAZOWIECKIE', 'OPOLSKIE', 'PODLASKIE',
                'POMORSKIE', 'PODKARPACKIE', 'ZACHODNIOPOMORSKIE', 'ŁÓDZKIE', 'WARMIŃSKO-MAZURSKIE']

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
          'November', 'December']


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
        self.classesdf = pd.read_csv('data/classes.csv')
        self.divisionsdf = pd.read_csv('data/divisions.csv')
        self.groupsdf = pd.read_csv('data/groups.csv')
        self.sections = pd.read_csv('data/sections.csv')
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

    def get3(self):
        return self.df[['MainAndCorrespondenceAreTheSame']].groupby('MainAndCorrespondenceAreTheSame')['MainAndCorrespondenceAreTheSame'].count()

    def get_target_by_month_and_voivod(self, month_value, voivod_value):
        month_filter = []
        voivod_filter = []
        if month_value is None:
            month_value = months
        if voivod_value is None:
            voivod_value = voivodeships
        for month in month_value:
            s = "MonthOfStartingOfTheBusiness == \"%s\"" % (month)
            month_filter.append(s)

        for voivod in voivod_value:
            s = "MainAddressVoivodeship == \"%s\"" % (voivod)
            voivod_filter.append(s)

        month_filter = " | ".join(month_filter)
        voivod_filter = " | ".join(voivod_filter)
        filtered_data = self.df.query(month_filter).query(voivod_filter)
        return filtered_data.groupby(['MonthOfStartingOfTheBusiness', 'Target']).size().unstack(fill_value=0).unstack()

    def get_data_by_month(self):
        target_by_month = self.df.groupby('MonthOfStartingOfTheBusiness')['Target']
        continued_by_month = self.df.query('Target == 0').groupby('MonthOfStartingOfTheBusiness')['Target'].count()
        non_continued_by_month = self.df.query('Target == 1').groupby('MonthOfStartingOfTheBusiness')['Target'].count()
        months = target_by_month.unique().index.values
        return months, continued_by_month, non_continued_by_month

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
    
    def get_mostTerminated(self):
        terminated = self.df[self.df.Target==1]
        allcount  = self.df.set_index('PKDMainSection').join(self.sections.set_index('pkdCode'))['section'].value_counts().rename_axis('pkdCode')
        
        terminatedRatio = terminated.set_index('PKDMainSection').join(self.sections.set_index('pkdCode'))['section'].value_counts().divide(allcount).multiply(100)
        return terminatedRatio

    def get_terminated_byNumberOfUniqueClasses(self):
        terminated = self.df[self.df.Target==1]
        terminatedPkdClasses = terminated["NoOfUniquePKDClasses"].value_counts().sort_index()
        allPkdClasses = self.df["NoOfUniquePKDClasses"].value_counts().sort_index()
        return terminatedPkdClasses.divide(allPkdClasses).fillna(0)

    def get_terminated_byNumberOfUniqueSections(self):
        terminated = self.df[self.df.Target==1]
        terminatedPkdSections = terminated["NoOfUniquePKDSections"].value_counts().sort_index()
        allPkdSections = self.df["NoOfUniquePKDSections"].value_counts().sort_index()
        return terminatedPkdSections.divide(allPkdSections).fillna(0)

    def get_terminated_byNumberOfAdditionalPlaceOfTheBusiness(self):
        terminated = self.df[self.df.Target==1]
        terminated = terminated["NoOfAdditionalPlaceOfTheBusiness"].value_counts().sort_index()
        all = self.df["NoOfAdditionalPlaceOfTheBusiness"].value_counts().sort_index()
        return terminated.divide(all).fillna(0)

    def get_terminated_byLicensePossesionRatio(self):
        terminated = self.df[self.df.Target==1]
        terminated = terminated["HasLicences"].value_counts().sort_index()
        all = self.df["HasLicences"].value_counts().sort_index()
        return terminated.divide(all).fillna(0)

    def get_terminated_byLicensePossesionAll(self):
        terminated = self.df[self.df.Target==1]
        terminated = terminated["HasLicences"].value_counts().sort_index()
        return terminated
        

    def get_terminated_byLicenseNumber(self):
        terminated = self.df[self.df.Target==1]
        terminated = terminated["NoOfLicences"].value_counts().sort_index()
        all = self.df["NoOfLicences"].value_counts().sort_index()
        return terminated.divide(all).fillna(0)

    def get_terminated_byDurationOfExistence(self):
        terminated = self.df[self.df.Target==1]
        terminated = terminated["DurationOfExistenceInMonths"].value_counts().sort_index()
        all = self.df["DurationOfExistenceInMonths"].value_counts().sort_index()
        return terminated.divide(all).fillna(0)


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
