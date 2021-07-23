import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

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
