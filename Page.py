from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_binary
import csv

driver = webdriver.Chrome()

yahoo_news_comments = []
start = 1
end =2

for page in range(start, end + 1):
    URL = "https://news.yahoo.co.jp/articles/c52e0e19641616fa6a69f1ec726f2fd0c68c2b96/comments"
    if page == 1:
        driver.get("https://news.yahoo.co.jp/articles/c52e0e19641616fa6a69f1ec726f2fd0c68c2b96/comments")
        get_coment_list = driver.find_elements(By.XPATH, "//p[@class='sc-esjcaD liAaGj']")
        print(driver.current_url)
    else:
        URL = URL + "?page={}".format(page)
        driver.get(URL)
        get_coment_list = driver.find_elements(By.XPATH, "//p[@class='sc-esjcaD liAaGj']")

    for comment in get_coment_list:
        yahoo_news_comments.append(comment)

for c in yahoo_news_comments:
    print(c.text)
    print('---------------------')

with open('comment.csv', 'w') as csv_file:
    fieldnames = ['comment']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for c in yahoo_news_comments:
        writer.writerow({'comment': c.text})