import pandas as pd
import os

os.chdir(os.path.abspath(os.path.dirname(__file__)))

siteid = pd.read_csv('../기상/기상관측소.csv',encoding='cp949')

for i in range(len(siteid)):

    daymet = pd.read_csv('../기상/'+siteid.iloc[i,1]+'.csv',parse_dates=[0],encoding='cp949')
    algae = pd.read_csv('../녹조/'+siteid.iloc[i,0]+'.csv',parse_dates=[0],encoding='cp949')

    algae.rename(columns={'조사일':'관측일'},inplace=True)

    df = pd.merge(daymet, algae, on='관측일', how='inner').sort_values(by='관측일').drop(columns='지점')
    df.drop(columns=['투명도','Microcystis', 'Anabaena', 'Oscillatoria', 'Aphanizomenon', '지오스민', '2MIB', 'Microcystin-LR (μg/L)'],inplace=True)

    df.to_csv(siteid.iloc[i,0]+'.csv',index=None,encoding='cp949')