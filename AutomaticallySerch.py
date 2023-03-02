import time
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import chromedriver_binary
import csv

driver = webdriver.Chrome()
yahoo_news_total_comments = []
yahoo_news_page_comments = []
page = 1

URL = "https://news.yahoo.co.jp/"

driver.get(URL)

elements = driver.find_elements(By.XPATH, "//div[@id='cmtrate']/ol[@class='yjnSub_list']")

print(type(elements))
print(len(elements))

for i, element in enumerate(elements):
    try:
        element.click()
        URL = driver.current_url
        driver.get(URL + "/comments")
        while (True):
            try:
                yahoo_news_page_comments = driver.find_elements(By.CSS_SELECTOR,
                                                                "p[class='UserCommentItem__Comment-eCuDbC ccpTzz']")
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
                    i += 1
            except NoSuchElementException:
                break

            time.sleep(5)

        print(len(yahoo_news_total_comments))
        with open(f'CSV/comment_2022_try_2022_11_16_No{i}.csv', 'w', newline='') as csv_file:
            fieldnames = ['comment']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for c in yahoo_news_total_comments:
                try:
                    writer.writerow({'comment': c})
                except UnicodeEncodeError:
                    continue
    except StaleElementReferenceException:
        print("お待ちください")