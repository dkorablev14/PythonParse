import requests
from bs4 import BeautifulSoup
import csv
import re

FILENAME = "hogwarts.csv"
columns = ["id", "mail", "gender", "real_name", "is_author"]
for i in range(17631, 471000):
    user = {}
    url = 'https://hogwartsnet.ru/mfanf/member.php?id=' + str(i)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    check_isset = soup.find('tr', {'class': 'wb top_fanf'}).text.strip()
    if check_isset == 'Запрашиваемый Вами автор не найден':
        continue
    centered = soup.find('div', {'class': 'CenteredContent'})
    tables = centered.find_all('table')
    nickname = tables[0].find('h2').text.strip()
    data = tables[1].find_all('tr')
    for tr in data:
        name = tr.find_all('td')[0].text.strip()
        value = tr.find_all('td')[1].text.strip()
        if name == 'E-mail:':
            user['mail'] = value
        elif name == 'Пол:':
            user['gender'] = value
        elif name == 'Настоящее имя':
            user['real_name'] = value
    if re.search('@', user['mail']) is None:
        continue
    check_author = tables[2].find('h1').text.strip()
    check_author_reg = re.search('У автора\\s+' + re.escape(nickname) + '\\s+(\\d+)', check_author).group(1)
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
