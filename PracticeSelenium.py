import time
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_binary
import csv

driver = webdriver.Chrome(ChromeDriverManager().install())
yahoo_news_total_comments = []
yahoo_news_page_comments = []
page = 1

URL = "https://news.yahoo.co.jp/articles/5b697b5a9fb5d8315b79f2ba0760c09c9acff872/comments"
file_name = 'CSV/2023_03_02/america_taityuuseisaku.csv'

# 1ページ以外でのURL
if not page == 1:
    URL = URL + "?page={}".format(page)
driver.get(URL)

while(True):
    try:
        yahoo_news_page_comments = driver.find_elements(By.CSS_SELECTOR, "p[class='UserCommentItem__Comment-eCuDbC ccpTzz']")
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
with open(file_name, 'w', newline='') as csv_file:
    fieldnames = ['comment']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for c in yahoo_news_total_comments:
        try:
            writer.writerow({'comment': c})
        except UnicodeEncodeError:
            continue
