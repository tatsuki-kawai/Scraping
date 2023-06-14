import time
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_binary
import csv
import os

driver = webdriver.Chrome(ChromeDriverManager().install())
yahoo_news_total_comments = []
yahoo_news_page_comments = []
page = 1

URL = "https://news.yahoo.co.jp/articles/1fc57bba01d74ad314a332858cbf76c4ba745522/comments"
folder_name = '2023_05_24'
csv_file_name = '20230524_1.csv'

folder_path = 'C:/Users/tatsuki/Desktop/program/TechnicalInvestigation/Data/yahoo/' + folder_name
csv_file_path = 'C:/Users/tatsuki/Desktop/program/TechnicalInvestigation/Data/yahoo/' + folder_name + '/' + csv_file_name


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
