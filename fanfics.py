import requests
from bs4 import BeautifulSoup
import csv
import re

FILENAME = "fanfics.csv"
columns = ["id", "mail", "gender", "real_name", "is_author", ""]
for i in range(1, 720000):
    user = {}
    url = 'https://fanfics.me/user' + str(i)
    r = requests.get(url)
    if r.status_code == 404:
        continue
    soup = BeautifulSoup(r.text, 'lxml')
    profileMain = soup.find('table', {'class': 'ProfileInfo_main'})
    trs = profileMain.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        if len(tds) > 1:
            name = tds[0].text.strip()
            value = tds[1].text.strip()
            if name == 'Реальное имя:':
                user['real_name'] = value
            elif name == 'Пол:':
                user['gender'] = value
    profile = soup.find('table', {'class': 'ProfileInfo'})
    trs = profile.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        if len(tds) > 1:
            name = tds[0].text.strip()
            value = tds[1].text.strip()
            if name == 'Email:':
                user['mail'] = value
            elif name == 'Другие сайты:':
                links = tds[1].find_all('a')
                # for link in links:
                #     link = link.get('href')
                #     link =
                # user['links']=links
    if re.search('@', user['mail']) is None:
        continue
    check_author = soup.find('div', {'class': 'fics_in_profile_container'})
    check_author_reg = re.search('У автора\\s+' + re.escape(user['name']) + '\\s+(\\d+)', check_author).group(1)
    if int(check_author_reg) != 0:
        user['is_author'] = True
    else:
        user['is_author'] = False
    print(i)
    user['id'] = i
    with open(FILENAME, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        if i == 1:
            writer.writeheader()
        writer.writerow(user)