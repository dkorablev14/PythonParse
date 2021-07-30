import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']


def disk():
    files = os.listdir('/home/aleks/PycharmProjects/funfuck/htmls/')
    # del files[0: files.index('398-1-0-6188.html')]
    # '398-1-0-6188.html'
    for file_name in files:
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
        folder_id = '19xqr9mADhozFKjXifZTcOzqxjtylXgv6'
        # name = file_name
        # file_path = '/home/aleks/PycharmProjects/funfuck/htmls/' + file_name
        # file_metadata = {
        #     'name': name,
        #     'parents': [folder_id]
        # }
        # media = MediaFileUpload(file_path, resumable=True)
        # r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        results = service.files().list(
            pageSize=1000,
            fields="nextPageToken, files(id, name, mimeType, parents, createdTime)",
            q="'"+folder_id+"' in parents").execute()
        files_disk = results['files']
        nextPageToken = results.get('nextPageToken')
        while nextPageToken:
            nextPage = service.files().list(
                pageSize=1000,
                fields="nextPageToken, files(id, name, mimeType, parents, createdTime)",
                q="'"+folder_id+"' in parents",
                pageToken=nextPageToken).execute()
            nextPageToken = nextPage.get('nextPageToken')
            files_disk = files_disk + nextPage['files']
        files_check = []
        for file in files_disk:
            if file['name'] in files_check:
                print(file['name'])
            else:
                files_check.append(file['name'])
