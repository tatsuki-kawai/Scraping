import random
import time
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import chromedriver_binary
import csv

driver = webdriver.Chrome()
categories = ['経済', "エンタメ", "スポーツ", "IT", "科学", "ライフ", "地域"]  # 取得したいカテゴリページ
# categories = ['経済']  # 取得したいカテゴリページ
total_news_list = []
total_news_data_list = []

# トップページに移動する
URL = "https://news.yahoo.co.jp/"
driver.get(URL)
print(driver.current_url)

# 各カテゴリからニュースの一覧と見出しを取得する
try:
    for category in categories:
        category_link = driver.find_element(By.LINK_TEXT, category)
        category_link.click()
        time.sleep(3)
        print(driver.current_url)

        # ニュースのリンク一覧の取得
        newsFeed_list = driver.find_element(By.CLASS_NAME, "newsFeed_list")
        news_list = newsFeed_list.find_elements(By.TAG_NAME, "a")
        news_link_list = [news.get_attribute("href") for news in news_list if news.get_attribute("href") is not None]

        total_news_list.extend(news_link_list)

except StaleElementReferenceException:
    print("画面が描画されていません")
except NoSuchElementException:
    print("要素がありません")
total_news_list = total_news_list[0:10]
for news_link in total_news_list:
    driver.get(news_link)
    try:
        print(driver.current_url)
        title = driver.find_element(By.CSS_SELECTOR, "h1[class='sc-gpHHfC fBLSKY']")
        # element = driver.find_element(By.CSS_SELECTOR, "div[class='sc-fcdeBU fwtBPB']")
        element = driver.find_element(By.CSS_SELECTOR, "p[class='sc-jtggT bAhgUU yjSlinkDirectlink highLightSearchTarget']")
        print(element.text)
        total_news_data_list.append({"title": title.text, "text": element.text})
    except NoSuchElementException:
        print("要素がありません")
        continue
    time.sleep(3)

# for news_data in total_news_data_list:
    # print(news_data)

with open('CSV/news_list/news_list_12_19.csv', 'w', newline='') as csv_file:
    fieldnames = ['title', 'text']
    writer = csv.DictWriter(csv_file, fieldnames)
    writer.writeheader()
    for news_data in total_news_data_list:
        try:
            writer.writerow(news_data)
        except UnicodeEncodeError:
            continue
