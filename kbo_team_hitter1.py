from selenium import webdriver
import time
import pandas as pd
from tqdm import tqdm
from selenium.webdriver.common.by import By

# 크롤링할 사이트
url = 'https://www.koreabaseball.com/Record/Team/Hitter/Basic1.aspx'

driver = webdriver.Chrome()
driver.implicitly_wait(3)
driver.get(url)

# 2001년부터 2023년까지 데이터 크롤링
year_list = [i for i in range(2001,2024)]
category_list = []
category_data_list = []

for year in tqdm(year_list):
    # 정규시즌으로 변경
    driver.find_element(By.CLASS_NAME, 'select02').click()
    xpath_format = '//option[@value="0"]'
    driver.find_element(By.XPATH, xpath_format.format(0)).click()
    time.sleep(0.5)
    # 연도 변경
    driver.find_element(By.CLASS_NAME, 'select03').click()
    xpath_format = '//option[@value="{year}"]'
    driver.find_element(By.XPATH, xpath_format.format(year=year)).click()
    time.sleep(0.1)

    # 데이터 가져오기
    temp_list = [x.split(' ') for x in driver.find_element(By.TAG_NAME,'table').text.split('\n')]
    temp_data = pd.DataFrame(columns=temp_list[0])

    # 데이터 프로임 만들기
    for i, temp in enumerate(temp_list[1:-1]):
        temp_data.loc[i] = temp
        time.sleep(0.5)
    temp_data['Year'] = year
    category_data_list.append(temp_data)
    time.sleep(0.1)
    time.sleep(1)

# csv 파일로 만들기
category_data = pd.concat(category_data_list)
category_data.to_csv('kbo_team_hitter1.csv', encoding='cp949', mode='w', index=True)
