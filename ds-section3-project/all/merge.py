import os
import pandas as pd
from glob import glob

os.chdir(os.path.abspath(os.path.dirname(__file__)))

dfs = []

for file in glob('*.csv'):

    df_ = pd.read_csv(file,encoding='cp949',parse_dates=[0])
    dfs.append(df_)

df = pd.concat(dfs)

df.columns = ['date','tavg','tmin','tmax','wt','pH','DO','NTU','chl-a','cyan']

df['month'] = df.date.dt.month.astype('str')

df.drop(['date'],axis=1,inplace=True)

df.dropna(inplace=True)

df.to_csv('merge.csv',index=None)