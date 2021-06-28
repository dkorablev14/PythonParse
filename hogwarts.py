import requests
from bs4 import BeautifulSoup
import csv
import re
for i in range(1,471000):
    user={}
    user_id=i
    url = 'https://hogwartsnet.ru/mfanf/member.php?id='+str(i)
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    centered=soup.find('div', {'class':'CenteredContent'})
    tables=centered.find_all('table')
    user['name']=tables[0].find('h2').text.strip()
    data=tables[1].find_all('tr')
    for tr in data:
        name=tr.find_all('td')[0].text.strip()
        value=tr.find_all('td')[1].text.strip()
        if(name=='E-mail:'):
            user['mail']=value
        elif(name=='Пол:'):
            user['gender']=value
        elif(name=='Настоящее имя'):
            user['real_name']=value
    check_author=tables[2].find('h1').text.strip()
    check_author_reg=re.match('\d+',check_author)
    # if(re.match('\d+',check_author))
    # res=parse_table(item)
    # with open('name.csv') as csvfile:
    #     reader = csv.DictReader(csvfile)
    # for row in reader:
    #     print(row['first_name'], row['last_name'])