from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import pandas as pd

url = str('https://www.mha.gov.sg/Newsroom/press-releases/Pages/press-releases.aspx')
browser = webdriver.Firefox()
browser.get(url)
html = browser.page_source

#http = urllib3.PoolManager()
#page = 11
#response = http.request('GET', url, preload_content=False)
#html = response.read()
soup = BeautifulSoup(html, 'lxml')
file = open('htmlprettified', 'w+')
file.write(soup.prettify())
final_table = []
import time

def tabulate_pressreleases(html_soup):
    global final_table

    list_date_tags = html_soup.findAll('div', {'class' : 'date js-date show'})
    list_title_tags = html_soup.findAll('h3')

    list_date = []
    list_title = []
    list_link = []

    for i in list_date_tags:
        date = re.search('(?<=>)[^<]+', str(i)).group()
        list_date.append(date)

    for i in list_title_tags:
        title = re.search('(?<=>)[^<]+', str(i)).group()
        list_title.append(title)

    for title_tag in list_title_tags:
        link_raw = title_tag.parent
        link = re.search('(?<=<a href=").+?(?=")', str(link_raw)).group()
        list_link.append(link)

    for i in range(len(list_date)):
        table_entry = {
            'date': list_date[i],
            'title': list_title[i],
            'link': list_link[i]
        }
        final_table.append(table_entry)

def tabulate_through():
    for i in range(68):
        global html
        global soup
        tabulate_pressreleases(soup)
        print(final_table)
        browser.find_element(By.XPATH, '//*[@id="PageLinkNext"]').click()
        time.sleep(2)
        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')

tabulate_through()
df = pd.DataFrame.from_dict(final_table)