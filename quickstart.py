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
    # https://web.archive.org/web/20190717194856/http://potter-fanfiction.ru:80/
    # http://nagini-snake.narod.ru/glavnaja.html
    for i in range(1, 2):
        # print(i)
        cookies = {
            'Cookie': 'onagini-snakeuzll=1626865286; ucvid=4HYBr148X9; _ym_uid=1626865283300121177; _ym_d=1626865283; _cc_session=2cd807a9-7d3a-4ea0-946f-79ac05eacf0c; sspUid=beca3287-2049-4439-ad60-a74f7a8ae463; dmpUid=ywmQT7kj94GqhafPSTXK; _ym_isad=2; onagini-snakedoubt=1; _cc_visit=1; _ym_visorc=b; _cc__visit_deep=12',
        }

        url = 'http://nagini-snake.narod.ru/index/fanfiki_2006/0-28'
        r = requests.get(url, cookies=cookies)
        if r.status_code == 404:
            continue
        soup = BeautifulSoup(r.text, 'lxml')
        tables = soup.find_all("ul", {'class': 'uMenuRoot'})
        years_all = tables[0].find_all('li')
        years_fun = []
        for years in years_all:
            if re.search('Фанфики', years.text.strip()) is not None:
                years = years.find('a').get('href')
                years_fun.append(years)
            else:
                continue
        for year in years_fun:
            url_card = 'http://nagini-snake.narod.ru' + year
            r_card = requests.get(url_card, cookies=cookies)
            soup_card = BeautifulSoup(r_card.text, 'lxml')
            content = soup_card.find_all('td', {'valign': 'top'})[1]
            hrefs_no = content.find_all('a')
            hrefs_yes = []
            for href in hrefs_no:
                if re.search('\/index\/', href):
                    hrefs_yes.append(href)
            for href in hrefs_yes:
                r_card = requests.get(url_card, cookies=cookies)
                soup_card = BeautifulSoup(r_card.text, 'lxml')
                content = soup_card.find_all('td', {'valign': 'top'})[1]
            file = url_card.split('load/')
            file = file[1].split('/')
            FILENAME = '/home/aleks/PycharmProjects/funfuck/htmls/' + file[-1] + ".html"
            r_card = requests.get(url_card)
            # time.sleep(2)
            if r_card.status_code == 404:
                continue

            with open(FILENAME, "w", encoding='utf-8') as file:
                file.write(str(content))
    # disk()


if __name__ == '__main__':
    main()
