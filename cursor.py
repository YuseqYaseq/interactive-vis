import pandas as pd


class Cursor:

    def __init__(self):
        self.df = pd.read_csv('data/ceidg_data_classif.csv', nrows=1000)

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


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('expand_frame_repr', False)
    classif = pd.read_csv('data/ceidg_data_classif.csv', nrows=1000)
    print(classif)

