import requests
from bs4 import BeautifulSoup
import csv
for i in range(1,471000):
    url = 'https://hogwartsnet.ru/mfanf/member.php?id='+str(i)
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    tables=soup.find_all('tr')
    # res=parse_table(item)
    # with open('name.csv') as csvfile:
    #     reader = csv.DictReader(csvfile)
    # for row in reader:
    #     print(row['first_name'], row['last_name'])