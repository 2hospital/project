from selenium import webdriver
import time
import os, shutil

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs',{'download.default_directory':os.path.abspath(os.path.dirname(__file__))})

driver = webdriver.Chrome('chromedriver',options=options)
driver.get('http://water.nier.go.kr/web/algaePreMeasure?pMENU_NO=111')

driver.find_element_by_xpath('/html/body/div[3]/div[2]/form[1]/div[2]/div[3]/a').click() #지점선택
time.sleep(2)
driver.find_element_by_xpath('/html/body/div[3]/div[2]/form[1]/div[2]/div[3]/div[1]/div[2]/div[1]/input[2]').click() # 수계로 찾기
time.sleep(1)

driver.find_element_by_xpath('/html/body/div[3]/div[2]/form[1]/div[2]/div[3]/div[1]/div[2]/div[3]/select[1]/option[3]').click() # 수계구분 낙동강

driver.find_element_by_xpath('/html/body/div[3]/div[2]/form[1]/div[2]/div[3]/div[1]/div[2]/div[1]/input[2]').click()
time.sleep(2)

driver.find_element_by_xpath('/html/body/div[3]/div[2]/form[1]/div[2]/div[3]/div[1]/div[2]/div[4]/a').click()
time.sleep(1)

driver.find_element_by_xpath('/html/body/div[3]/div[2]/form[1]/div[2]/div[3]/div[1]/div[3]/div[1]/div/div/div[1]/table/thead/tr[1]/th[1]/div/input').click()
time.sleep(1)

driver.find_element_by_xpath('/html/body/div[3]/div[2]/form[1]/div[2]/div[3]/div[1]/div[4]/a[1]').click()
time.sleep(1)

for i in range(1,9): #2014~2021
    driver.find_element_by_xpath(f'/html/body/div[3]/div[2]/form[1]/div[2]/div[2]/select[2]/option[{str(i)}]').click() #시작연도
    driver.find_element_by_xpath('/html/body/div[3]/div[2]/form[1]/div[2]/div[2]/select[3]/option[1]').click() #시작월
    driver.find_element_by_xpath(f'/html/body/div[3]/div[2]/form[1]/div[2]/div[2]/select[4]/option[{str(i)}]').click()
    driver.find_element_by_xpath('/html/body/div[3]/div[2]/form[1]/div[2]/a').click()
    time.sleep(5)
    
    driver.find_element_by_xpath('/html/body/div[3]/div[2]/form[1]/div[3]/div/a[2]').click()
    time.sleep(5)

    filepath = r'C:\Users\user\OneDrive - UOS\codestates\ds-section3-project\녹조'
    filename = max([filepath + os.sep + f for f in os.listdir(filepath)], key=os.path.getctime)
    shutil.move(os.path.join(filepath, filename), f'algae_{2022-i}.csv')
    time.sleep(10)