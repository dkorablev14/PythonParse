import requests
from bs4 import BeautifulSoup
import csv
import re

FILENAME = "fanfics.csv"
columns = ["id", "mail", "gender", "real_name", "is_author", "links"]
for i in range(123993, 720000):
    user = {}
    url = 'https://fanfics.me/user' + str(i)
    r = requests.get(url)
    if r.status_code == 404:
        continue
    soup = BeautifulSoup(r.text, 'lxml')
    profileMain = soup.find('table', {'class': 'ProfileInfo_main'})
    if profileMain is None:
        continue
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
    if profile is None:
        continue
    trs = profile.find_all('tr')
    user['links'] = []
    user['mail'] = ''
    for tr in trs:
        tds = tr.find_all('td')
        if len(tds) > 1:
            name = tds[0].text.strip()
            value = tds[1].text.strip()
            if name == 'Email:':
                user['mail'] = value
            elif name == 'Другие сайты:':
                links = tds[1].find_all('a')
                for link in links:
                    link = link.get('href')
                    link = link.rpartition('php?url=')
                    if re.search('vk\\.com|www\\.diary\\.ru|ficbook\\.net|hogwartsnet\\.ru', link[2]) is not None:
                        user['links'].append(link[2])
    if user['mail'] == '' or re.search('@', user['mail']) is None:
        continue
    # if len(user['links']) > 0:
    user['links'] = ','.join(user['links'])
    check_author = soup.find('div', {'class': 'fics_in_profile_container'})
    if check_author is None:
        check_author_reg = 0
    else:
        check_author = check_author.find('div', {'class': 'ProfileLeft_h2_descr'}).text.strip()
        check_author_reg = re.search('\\d+', check_author).group(0)
    if int(check_author_reg) != 0:
        user['is_author'] = True
    else:
        user['is_author'] = False
    print(i)
    user['id'] = i
    with open(FILENAME, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        if i == 2:
            writer.writeheader()
        writer.writerow(user)
