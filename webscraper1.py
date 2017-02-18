#newlinefornewcommit
from bs4 import BeautifulSoup
import urllib3
import re

file = open('prettified_html', 'w')

http = urllib3.PoolManager()
page = 11
url = str('https://www.mha.gov.sg/Newsroom/press-releases/Pages/press-releases.aspx')
print(url)
response = http.request('GET', url, preload_content=False)
html = response.read()
soup = BeautifulSoup(html, 'lxml')

file.write(soup.prettify())
final_table = []

def tabulate_pressreleases(html_soup):
    global final_table
    table = soup.findAll('tr')
    for i in table:
        table_entry = {
            'date': 'blank',
            'title': 'blank',
            'link': 'blank'
        }
        table_entry['date'] = re.search('(?<=string;#)[^<]+', str(i)).group()
        table_entry['title'] = re.search('(?<=">).+?(?=</a>)', str(i)).group()
        table_entry['link'] = re.search('(?<=<a href=").+?(?=">)', str(i)).group()
        final_table.append(table_entry)

for i in range(60):
    global page
    print(url)
    response = http.request('GET', url, preload_content=False)
    html = response.read()
    soup = BeautifulSoup(html, 'lxml')
    tabulate_pressreleases(soup)
    page += 10
    print(page)
    print(final_table)
# print(final_table)
# print(len(final_table))
# print(final_table)

# print(response.status)
# print(soup.headers)
# print(soup.prettify())