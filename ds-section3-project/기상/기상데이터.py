import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime

os.chdir(os.path.abspath(os.path.dirname(__file__)))

key = 'e6567dd09dbc244edd15884134bac0c4a6b6427594'
output = 'xml'

site = pd.read_csv('기상관측소.csv',encoding='cp949')

start = '20050101'
end = datetime.now().strftime('%Y%m%d')

for i,j in enumerate(tqdm(site['근접관측소코드(기상)'],position=0,leave=True)):
    
    current = start
    infor = {} 
              
    queryParams = 'ServiceKey='+key+'&obscd='+str(j)+'&startdt='+start+'&enddt='+end+'&output='+output
    
    url = 'http://www.wamis.go.kr:8080/wamis/openapi/wkw/we_dtdata?'+queryParams
    
    req = requests.get(url,allow_redirects=False)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    
    items = ['ymd','taavg','tamin','tamax']
    items_name = ['관측일','평균기온','최저기온','최고기온']
               
    for each in items:
        finded = soup.find_all(each)
    
        if infor.get(each) is None:
            infor[each] = [x.text for x in finded]
        else:
            infor[each] = infor[each] + [x.text for x in finded]
   
    prcp = pd.DataFrame(infor)
    prcp.columns = items_name
    
    prcp.to_csv(site['근접관측소명(기상)'][i]+'.csv',index=None,encoding='cp949')