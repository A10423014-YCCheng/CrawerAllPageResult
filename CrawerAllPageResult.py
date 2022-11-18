import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import datetime

s = Service(r"C:\chromedriver.exe")
driver = webdriver.Chrome(service=s)
df_column = ['書名','出版日期','價格','狀態','圖片網址']
df = pd.DataFrame(columns=df_column)

###進入天瓏並搜尋selenium，書名/出版日期/價格/狀態/小圖片網址(到.jpg就好)放在panads###
url = 'https://www.tenlong.com.tw/search?utf8=%E2%9C%93&keyword=selenium'
driver.get(url)


while True:

    element_name = driver.find_elements(By.XPATH, '//strong/a')
    element_date = driver.find_elements(By.XPATH, '//span[@class = "publish-date"]')
    element_price = driver.find_elements(By.XPATH, '//span[@class = "price"]')
    element_status = driver.find_elements(By.XPATH, '//span[@class = "status"]')
    element_link = driver.find_elements(By.XPATH, '//a[@class = "cover w-full"]/img')
    try:
        nextpage = driver.find_element(By.XPATH, '//a[@class = "next_page"]')
    except Exception:
        nextpage = None
    list_2D = []
    for i in range(len(element_name)):
        try:
            date = datetime.datetime.strptime(element_date[i].text.split('：')[1],'%Y-%m-%d')
        except Exception:
            continue
        price = int(element_price[i].text.replace('$','').replace(',',''))
        link = element_link[i].get_attribute('src').split('?')[0]
        list_2D.append([element_name[i].text, date, price,
                        element_status[i].text, link])

    df1 = pd.DataFrame(list_2D, columns=df_column)
    df = pd.concat([df,df1])
    if (nextpage is None):
        break
    else:
        driver.get(nextpage.get_attribute('href'))
    time.sleep(3)
driver.quit()

df.to_excel(r'D:\Python\Program\DB and Web crawler\20221116\Result.xlsx', index = False)