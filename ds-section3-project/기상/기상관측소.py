import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
import numpy as np

folder_path = os.path.abspath(os.path.dirname(__file__))
os.chdir(folder_path)

key = 'e6567dd09dbc244edd15884134bac0c4a6b6427594'
basin = '2'
output = 'xml'

queryParams = 'ServiceKey='+key+'&basin='+basin+'&output='+output
url = 'http://www.wamis.go.kr:8080/wamis/openapi/wkw/we_dwtwtobs?'+queryParams
req = requests.get(url,allow_redirects=False)
html = req.text
soup = BeautifulSoup(html, 'html.parser')

items = ['obscd','obsnm']

infor = {}

for each in items:
    finded = soup.find_all(each)

    if infor.get(each) is None:
        infor[each] = [x.text for x in finded]
    else:
        infor[each] = infor[each] + [x.text for x in finded]

queryParams = 'ServiceKey='+key+'&basin='+basin+'&output='+output
url = 'http://www.wamis.go.kr:8080/wamis/openapi/wkw/we_dwtwtobs?'+queryParams
req = requests.get(url,allow_redirects=False)
html = req.text
soup = BeautifulSoup(html, 'html.parser')

siteid = infor['obscd']
items = ['lat','lon']

for site in siteid:
    
    queryParams = 'ServiceKey='+key+'&obscd='+str(site)+'&output='+output
    url = 'http://www.wamis.go.kr:8080/wamis/openapi/wkw/we_obsinfo?'+queryParams
    req = requests.get(url,allow_redirects=False)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    for each in items:
        finded = soup.find_all(each)
    
        if infor.get(each) is None:
            infor[each] = [x.text for x in finded]
        else:
            infor[each] = infor[each] + [x.text for x in finded]


items_name = ['관측소코드','관측소명','위도','경도']

df = pd.DataFrame(infor)
df.columns = items_name

algae = pd.read_csv('../녹조/관측지점위경도.txt',sep='/',header=None,names=['녹조관측지점','경도','위도']) # from 조류경보제 운영 매뉴얼(2020), 국립환경과학원
df = pd.read_csv('기상관측소.csv',encoding='cp949')

# 위경도 시분초 좌표계 -> GPS 좌표계 변환
algae['경도'] = algae['경도'].map(lambda x: int(x.split('-')[0])+int(x.split('-')[1])/60+float(x.split('-')[2])/3600)
algae['위도'] = algae['위도'].map(lambda x: int(x.split('-')[0])+int(x.split('-')[1])/60+float(x.split('-')[2])/3600)


# 녹조관측지점과 기상관측지점의 위치가 같지 않으므로 가장 가까운 위치로 선정
def getclosest_ij(lats,lons,latpt,lonpt):
      
      dist_sq = (lats-latpt)**2 + (lons-lonpt)**2 
      minindex_flattened = dist_sq.argmin()
      
      return np.unravel_index(minindex_flattened, lats.shape)

latvals = df['위도']
lonvals = df['경도']

idx = []

for i in range(len(algae)):
    
    loni = algae.loc[i,'경도']
    lati = algae.loc[i,'위도']
    
    idx.append(getclosest_ij(latvals,lonvals,lati,loni)[0])

station = []
station_code = []

for i in idx:
    
    station.append(df['관측소명'][i])
    station_code.append(df['관측소코드'][i])

result = pd.DataFrame([algae['녹조관측지점'].tolist(),station,station_code],index=['녹조관측지점','근접관측소명(기상)','근접관측소코드(기상)']).T

result.loc[0:1,'근접관측소명(기상)'] = '대구' # 대구(기)의 경우 2016 이후의 데이터가 없음
result.loc[0:1,'근접관측소코드(기상)'] = '20121143' # 대구(기)의 경우 2016 이후의 데이터가 없음

result.to_csv('기상관측소.csv',index=None,encoding='cp949')