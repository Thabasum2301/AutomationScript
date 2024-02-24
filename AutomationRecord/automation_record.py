import os

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']


def authenticate():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def upload_file(file_path, drive_service):
    file_name = os.path.basename(file_path)

    file_metadata = {'name': file_name}

    mime_type = 'application/octet-stream'

    media = MediaFileUpload(file_path, mimetype=mime_type)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    print('File ID: %s' % file.get('id'))

def upload_directory(directory_path, drive_service):

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            upload_file(file_path, drive_service)

def main():
    creds = authenticate()

    service = build('drive', 'v3', credentials=creds)

    directory_path = 'filesToUpload'

    upload_directory(directory_path, service)

if __name__ == '__main__':
    main()
