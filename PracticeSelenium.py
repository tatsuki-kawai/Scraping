import csv
import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome()

yahoo_news_total_comments = []
yahoo_news_page_comments = []
page = 1

URL = "https://news.yahoo.co.jp/articles/878360dc0a31e409bec1febc5c31c1a9dd0713e2/comments"
folder_name = '2023_06_14'
csv_file_name = '20230614_1.csv'

# folder_path = 'C:/Users/tatsuki/Desktop/program/TechnicalInvestigation/Data/yahoo/' + folder_name
folder_path = 'CSV/' + folder_name
# csv_file_path = 'C:/Users/tatsuki/Desktop/program/TechnicalInvestigation/Data/yahoo/' + folder_name + '/' + csv_file_name
csv_file_path = 'CSV/' + folder_name + '/' + csv_file_name


# 1ページ以外でのURL
if not page == 1:
    URL = URL + "?page={}".format(page)
driver.get(URL)

while(True):
    try:
        yahoo_news_page_comments = driver.find_elements(By.CSS_SELECTOR, "p[class='UserCommentItem__Comment-eoheEU cTIZmn']")
        print(driver.current_url)
        for c in yahoo_news_page_comments:
            print(c.text)
            print('---------------------')
            yahoo_news_total_comments.append(c.text)

        i = 0
        while i < 3:
            try:
                driver.find_element(By.LINK_TEXT, "次へ").click()
                break
            except StaleElementReferenceException:
                print("おまちください")
                driver.back()
            i += 1
    except NoSuchElementException:
        break

    time.sleep(10)

print(len(yahoo_news_total_comments))

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

with open(csv_file_path, 'w', newline='') as csv_file:
    fieldnames = ['comment']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for c in yahoo_news_total_comments:
        try:
            writer.writerow({'comment': c})
        except UnicodeEncodeError:
            continue
