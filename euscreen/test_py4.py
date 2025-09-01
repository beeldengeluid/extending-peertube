import os
import requests
from tqdm import tqdm

# === Configuration ===
PEERTUBE_URL = 'https://peertube.beeldengeluid.nl'
ACCESS_TOKEN = '1bf3896bf9058b376138ade2e80d4b4184633fea'
CHANNEL_ID = '696'
VIDEO_DIR = 'C:\\Users\\clatronico\\Documents\\PEERTUBE\\test' #to be edited 
PLAYLIST_ID = '1341'  # <-- Replace this with your actual playlist ID

UPLOAD_URL = f'{PEERTUBE_URL}/api/v1/videos/upload'
ADD_TO_PLAYLIST_URL = f'{PEERTUBE_URL}/api/v1/video-playlists/{PLAYLIST_ID}/videos'

DEFAULT_PRIVACY = 2
DOWNLOADABLE = False

def upload_video(file_path, name, description='Uploaded via script'):
    mime_type = 'video/mp4'

    with open(file_path, 'rb') as video_file:
        files = {
            'videofile': (os.path.basename(file_path), video_file, mime_type)
        }
        data = {
            'name': name,
            'channelId': CHANNEL_ID,
            'description': description,
            'privacy': DEFAULT_PRIVACY,
            'downloadEnabled': str(DOWNLOADABLE).lower()
        }
        headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}

        print(f"\nUploading '{name}' to PeerTube...")

        response = requests.post(UPLOAD_URL, headers=headers, files=files, data=data)

        if response.status_code == 200:
            response_json = response.json()
            video_id = response_json['video']['id']
            print(f"✅ Uploaded: {name}, Video ID: {video_id}")
            add_video_to_playlist(video_id)
            return response_json
        else:
            print(f"❌ Failed to upload {name}. Status: {response.status_code}")
            print(response.text)
            return None

def add_video_to_playlist(video_id):
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    data = {'videoId': video_id}

    print(f"Adding video ID {video_id} to playlist ID {PLAYLIST_ID}...")

    response = requests.post(ADD_TO_PLAYLIST_URL, headers=headers, json=data)

    if response.status_code == 200:
        print(f"✅ Video ID {video_id} successfully added to playlist.")
    else:
        print(f"❌ Failed to add video ID {video_id} to playlist. Status: {response.status_code}")
        print(response.text)

for filename in os.listdir(VIDEO_DIR):
    if filename.lower().endswith('.mp4'):
        filepath = os.path.join(VIDEO_DIR, filename)
        video_name = os.path.splitext(filename)[0]
        upload_video(filepath, video_name)
