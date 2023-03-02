import random
import time
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import chromedriver_binary
import csv

driver = webdriver.Chrome()
categories = ['主要', '国内', '国際', '経済', "エンタメ", "スポーツ", "IT", "科学", "ライフ", "地域"]  # 取得したいカテゴリページ
# categories = ['経済']  # 取得したいカテゴリページ

total_news_list = []
total_news_data_list = []


# トップページに移動する
URL = "https://news.yahoo.co.jp/topics/top-picks"
driver.get(URL)
print(driver.current_url)

# 各カテゴリからニュースの一覧と見出しを取得する
for category in categories:
    try:
        news_link_list = []
        # category_link_list = driver.find_element(By.CSS_SELECTOR, "ul[class='sc-jkPxnQ dsgZle']")
        # category_link = category_link_list.find_element(By.LINK_TEXT, category)
        category_link = driver.find_element(By.LINK_TEXT, category)
        category_link.click()
        time.sleep(3)
        print(driver.current_url)
        while True:
            print(driver.current_url)
            # ニュースのリンク一覧の取得
            newsFeed_list = driver.find_element(By.CLASS_NAME, "newsFeed_list")
            news_list = newsFeed_list.find_elements(By.TAG_NAME, "a")

            for news in news_list:
                if news.get_attribute("href") is not None:
                    if news.get_attribute("href") not in news_link_list:
                        news_link_list.append(news.get_attribute("href"))

            if len(news_link_list) > 100:
                break
            try:
                # next_link = driver.find_element(By.LINK_TEXT, 'もっと見る')
                next_link = driver.find_element(By.CSS_SELECTOR, "div[class='sc-iybRtq fCDGYX newsFeed_more']")
                button = next_link.find_element(By.TAG_NAME, "button")
                button.click()
                time.sleep(5)
            except NoSuchElementException:
                break

        for news_link in news_link_list:
            total_news_list.append([news_link, category])
    except StaleElementReferenceException:
        print("画面が描画されていません")
    except NoSuchElementException:
        print("要素がありません")

print(len(total_news_list))
# total_news_list = total_news_list[0:10]

for news in total_news_list:
    try:
        URL = news[0]
        category = news[1]
        driver.get(URL)
        #「ここがポイント」みたいなやつとアンケート調査しているやつに関してはページの作りが対応してないからかテキストがとれない。
        print(driver.current_url)
        title = driver.find_element(By.CSS_SELECTOR, "h1[class='sc-gpHHfC fBLSKY']")
        # element = driver.find_element(By.CSS_SELECTOR, "div[class='sc-fcdeBU fwtBPB']")
        p_list = driver.find_elements(By.CSS_SELECTOR, "p[class='sc-jtggT bAhgUU yjSlinkDirectlink highLightSearchTarget']")
        text = ""
        for element in p_list:
            text += element.text
        print(text)
        total_news_data_list.append({"title": title.text, "category": category, "text": text})
    except NoSuchElementException:
        print("要素がありません")
        continue
    except TimeoutException:
        print("タイムアウトしました")
        time.sleep(3)
        continue

# for news_data in total_news_data_list:
    # print(news_data)

with open('CSV/news_list/news_list_12_20_business_topic_1000.csv', 'w', newline='') as csv_file:
    fieldnames = ['title', 'category', 'text']
    writer = csv.DictWriter(csv_file, fieldnames)
    writer.writeheader()
    for news_data in total_news_data_list:
        try:
            writer.writerow(news_data)
        except UnicodeEncodeError:
            continue
