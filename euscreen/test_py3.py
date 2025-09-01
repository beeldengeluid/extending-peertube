import os
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# === Configuration ===
PEERTUBE_URL = 'https://peertube.beeldengeluid.nl'
ACCESS_TOKEN = '819f28fa48c455d7f0292499f4928a124f4431f5'  # Replace with your token
CHANNEL_ID = '696'      # Replace with your channel ID
VIDEO_DIR = 'C:\\Users\\clatronico\\Desktop\\test'#to be edited with correct 

UPLOAD_URL = f'{PEERTUBE_URL}/api/v1/videos/upload'

DEFAULT_PRIVACY = 2  # 1=Public, 2=Unlisted, 3=Private
DOWNLOADABLE = False  # Prevent downloads

def upload_video(file_path, name, description='Uploaded via script'):
    mime_type = 'video/mp4'  # explicitly set for mp4 files; adjust if needed

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
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}'
        }

        print(f"\nUploading '{name}' with headers: {headers}")
        print(f"Payload data: {data}")
        print(f"File tuple: {files['videofile'][0]}, MIME type: {files['videofile'][2]}")

        response = requests.post(UPLOAD_URL, headers=headers, files=files, data=data)

        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")

        if response.status_code == 200:
            print(f"✅ Successfully uploaded: {name}")
            return response.json()
        else:
            print(f"❌ Failed to upload {name}")
            return None

for filename in os.listdir(VIDEO_DIR):
    if filename.lower().endswith('.mp4'):
        filepath = os.path.join(VIDEO_DIR, filename)
        video_name = os.path.splitext(filename)[0]
        upload_video(filepath, video_name)
