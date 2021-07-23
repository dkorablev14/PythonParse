from __future__ import print_function
import requests
from bs4 import BeautifulSoup
import re
from functions import disk
import os
import time


def main():
    text()
    # disk()


def text():
    for i in range(1, 486):
        print(i)
        url = 'http://fanfics.info/load/?page' + str(i)
        r = requests.get(url)
        # time.sleep(5)
        if r.status_code == 404:
            continue
        soup = BeautifulSoup(r.text, 'lxml')
        entries = soup.find_all("div", id=re.compile('entryID\\d+'))
        for entry in entries:
            title = entry.find_all('table')
            url_card = title[1].find('a')
            url_card = 'https://fanfic.ucoz.com' + url_card.get('href')
            file = url_card.split('load/')
            FILENAME = 'C:/Users/Denis/PycharmProjects/FunFuck2/htmls/' + file[1] + ".html"
            r_card = requests.get(url_card)
            # time.sleep(2)
            if r_card.status_code == 404:
                continue
            soup_card = BeautifulSoup(r_card.text, 'lxml')
            content = soup_card.find('div', {'class': 'content'})
            with open(FILENAME, "w", encoding='utf-8') as file:
                file.write(str(content))
        # profile = soup.find('table', {'class': 'ProfileInfo'})
        # if profile is None:
        #     continue
        # trs = profile.find_all('tr')
        # user['links'] = []
        # user['mail'] = ''
        # for tr in trs:
        #     tds = tr.find_all('td')
        #     if len(tds) > 1:
        #         name = tds[0].text.strip()
        #         value = tds[1].text.strip()
        #         if name == 'Email:':
        #             user['mail'] = value
        #         elif name == 'Другие сайты:':
        #             links = tds[1].find_all('a')
        #             for link in links:
        #                 link = link.get('href')
        #                 link = link.rpartition('php?url=')
        #                 if re.search('vk\\.com|www\\.diary\\.ru|ficbook\\.net|hogwartsnet\\.ru', link[2]) is not None:
        #                     user['links'].append(link[2])
        # if user['mail'] == '' or re.search('@', user['mail']) is None:
        #     continue
        # if len(user['links']) > 0:
        # user['links'] = ','.join(user['links'])
        # check_author = soup.find('div', {'class': 'fics_in_profile_container'})
        # if check_author is None:
        #     check_author_reg = 0
        # else:
        #     check_author = check_author.find('div', {'class': 'ProfileLeft_h2_descr'}).text.strip()
        #     check_author_reg = re.search('\\d+', check_author).group(0)
        # if int(check_author_reg) != 0:
        #     user['is_author'] = True
        # else:
        #     user['is_author'] = False
        # user['id'] = i


if __name__ == '__main__':
    main()
