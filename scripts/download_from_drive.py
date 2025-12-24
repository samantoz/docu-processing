import os
import io
import argparse
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
from pathlib import Path

class GoogleDriveDownloader:
    """
    A modular class for downloading files from Google Drive.
    """

    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

    def __init__(self, credentials_path='credentials.json', token_path='token.pickle'):
        """
        Initialize the downloader with paths to credentials and token files.

        :param credentials_path: Path to the credentials.json file from Google Cloud Console.
        :param token_path: Path to store the OAuth token.
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None

    def authenticate(self):
        """
        Authenticate with Google Drive API using OAuth2.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens.
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('drive', 'v3', credentials=creds)

    def download_file(self, file_id, local_path):
        """
        Download a file from Google Drive to the specified local path.

        :param file_id: The ID of the file on Google Drive.
        :param local_path: The local path where to save the file.
        """
        if not self.service:
            raise Exception("Service not authenticated. Call authenticate() first.")

        request = self.service.files().get_media(fileId=file_id)
        with io.FileIO(local_path, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%.", end='\r')
        print()
    def get_file_metadata(self, file_id):
        """
        Get metadata of a file from Google Drive.

        :param file_id: The ID of the file.
        :return: File metadata dictionary.
        """
        if not self.service:
            raise Exception("Service not authenticated. Call authenticate() first.")

        return self.service.files().get(fileId=file_id, fields='name, mimeType').execute()

    @staticmethod
    def create_folder_if_not_exists(folder_path):
        """
        Create a folder if it does not exist.

        :param folder_path: The path to the folder.
        """
        path = Path(folder_path)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"Created folder: {folder_path}")

def download_from_drive(file_id, subfolder_name, base_path='data/docs', credentials_path='credentials.json', token_path='token.pickle'):
    """
    Function to download a file from Google Drive into a subfolder under base_path.

    :param file_id: The Google Drive file ID.
    :param subfolder_name: The name of the subfolder under base_path.
    :param base_path: The base path for downloads (default: 'data/docs').
    :param credentials_path: Path to the credentials.json file.
    :param token_path: Path to the token.pickle file.
    """
    downloader = GoogleDriveDownloader(credentials_path=credentials_path, token_path=token_path)
    downloader.authenticate()

    subfolder_path = Path(base_path) / subfolder_name
    GoogleDriveDownloader.create_folder_if_not_exists(subfolder_path)

    # Get file metadata to get the name
    metadata = downloader.get_file_metadata(file_id)
    file_name = metadata['name']

    # Download the file
    local_path = subfolder_path / file_name
    print(f"Starting download of '{file_name}' to '{local_path}'...")
    downloader.download_file(file_id, local_path)
    print(f"Successfully downloaded '{file_name}' to '{local_path}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a file from Google Drive.")
    parser.add_argument("file_id", help="The ID of the file on Google Drive.")
    parser.add_argument("subfolder_name", help="The name of the subfolder to download the file into.")
    parser.add_argument("--base-path", default="data/docs", help="The base path for downloads (default: 'data/docs').")
    parser.add_argument("--credentials", default="credentials.json", help="Path to the credentials.json file.")
    parser.add_argument("--token", default="token.pickle", help="Path to the token.pickle file.")
    
    args = parser.parse_args()

    download_from_drive(args.file_id, args.subfolder_name, args.base_path, args.credentials, args.token)