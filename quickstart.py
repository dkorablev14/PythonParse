from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import requests
from bs4 import BeautifulSoup
import re
import os
import time

SCOPES = ['https://www.googleapis.com/auth/drive']


def disk():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('drive', 'v3', credentials=creds)
    # folder_id = '1ZBmq347E0sLTrG9-w4ZUPI2nB72uKham'
    results = service.files().list(
        pageSize=1000,
        fields="nextPageToken, files(id, name, mimeType, parents, createdTime)",
        q="'1ZBmq347E0sLTrG9-w4ZUPI2nB72uKham' in parents").execute()
    files = results['files']
    nextPageToken = results.get('nextPageToken')
    while nextPageToken:
        nextPage = service.files().list(
            pageSize=1000,
            fields="nextPageToken, files(id, name, mimeType, parents, createdTime)",
            q="'1ZBmq347E0sLTrG9-w4ZUPI2nB72uKham' in parents",
            pageToken=nextPageToken).execute()
        nextPageToken = nextPage.get('nextPageToken')
        files = files + nextPage['files']
    files_check = []
    for file in files:
        if file['name'] in files_check:
            print(file['name'])
        else:
            files_check.append(file['name'])
# files = os.listdir('C:/Users/Denis/PycharmProjects/FunFuck2/htmls')
# del files[0: files.index('398-1-0-6188.html')]
# '398-1-0-6188.html'
# for file_name in files:
#     name = file_name
#     file_path = 'C:/Users/Denis/PycharmProjects/FunFuck2/htmls/' + file_name
#     file_metadata = {
#         'name': name,
#         'parents': [folder_id]
#     }
#     media = MediaFileUpload(file_path, resumable=True)
#     r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()


def main():
    # text()
    disk()


def text():
    for i in range(337, 338):
        print(i)
        url = 'https://fanfic.ucoz.com/load/?page' + str(i)
        r = requests.get(url)
        # time.sleep(5)
        if r.status_code == 404:
            continue
        soup = BeautifulSoup(r.text, 'lxml')
        entries = soup.find_all("div", id=re.compile('entryID\\d+'))
        for entry in entries:
            title = entry.find('div', {'class': 'eTitle'})
            url_card = title.find('a')
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
