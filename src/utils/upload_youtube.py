#!/usr/bin/env python3
"""
Upload video to YouTube using YouTube Data API v3
"""

import argparse
import os
import yaml
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']


def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)


def get_authenticated_service():
    """Authenticate with YouTube API"""
    creds = None

    # Saved token from previous authentications
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for next time
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('youtube', 'v3', credentials=creds)


def upload_video(video_path, title, description="", tags=None, category="10", privacy="public"):
    """Upload video to YouTube"""

    print(f"📤 Starting upload to YouTube...")
    print(f"   Título: {title}")

    youtube = get_authenticated_service()

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags or [],
            'categoryId': category
        },
        'status': {
            'privacyStatus': privacy,
            'selfDeclaredMadeForKids': False
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"   Progress: {int(status.progress() * 100)}%")

    video_id = response['id']
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    print(f"✅ Upload complete!")
    print(f"🔗 URL: {video_url}")

    return video_url


def main():
    parser = argparse.ArgumentParser(description='Upload video to YouTube')
    parser.add_argument('--video', type=str, required=True, help='Video path')
    parser.add_argument('--title', type=str, required=True, help='Video title')
    parser.add_argument('--description', type=str, default='', help='Video description')
    parser.add_argument('--tags', type=str, help='Comma-separated tags')
    parser.add_argument('--privacy', type=str, default='public', choices=['public', 'private', 'unlisted'])

    args = parser.parse_args()

    tags = args.tags.split(',') if args.tags else []

    upload_video(
        args.video,
        args.title,
        args.description,
        tags,
        privacy=args.privacy
    )


if __name__ == "__main__":
    main()
