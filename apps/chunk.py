import numpy as np
import datetime
import time
import calendar
import pandas as pd
h = calendar.month
terrorism = pd.read_csv('data/global_terror.csv',
                        encoding='latin-1', low_memory=False,
                        usecols=['iyear', 'imonth', 'iday', 'country_txt', 'city', 'longitude', 'latitude',
                        'nkill', 'nwound', 'summary', 'target1', 'gname','region_txt','provstate'])


years = [c for c in range(2010,2019)]
print(years[0])
print(terrorism['iyear'].head())



# a = [str(c) if (c > years[0] & c < years[1]) else '' for c in years]


a = [c if c >= years[0] & c < years[1] else False for c in years]
print(a)