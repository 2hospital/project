import os
import pandas as pd
from glob import glob

folder_path = os.path.abspath(os.path.dirname(__file__))
os.chdir(folder_path)

dfs = []

for data in glob('algae_*.csv'):
    df = pd.read_csv(data,encoding='cp949')
    
    dfs.append(df)
    
df = pd.concat(dfs)

df['채수위치'] = df['채수위치'].map(lambda x: x.replace('·',',') if '·' in x else x)

df['지점'] = df['지점명']+'('+df['채수위치']+')'
df.drop(['지점명','분류','채수위치'],axis=1,inplace=True)

for site in df['지점'].unique():
    
    df_site = df[df['지점'] == site]
    df_site.sort_values(by='조사일')
    
    df_site.to_csv(site+'.csv',index=None,encoding='cp949')