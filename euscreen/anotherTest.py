from flask import Flask, jsonify, request, abort
import requests

app = Flask(__name__)

# === CONFIGURATION ===
PEERTUBE_URL = 'https://peertube.beeldengeluid.nl'
CHANNEL_ID = '41vzdcnxkn1ar7q5xitrtg1x3yr725ua'             # ← Replace this
PEERTUBE_TOKEN = 'e3ccb2367aac227ec023cb1c2d7c3df143bada76'     # ← Replace this
SHARED_API_SECRET = 'bM6jkBTJkL5jmVby3BlJUlXYQuVSocQJ'       # ← Change this to something private

@app.route('/video-feed')
def get_video_urls():
    # === Require secret token in query string
    client_secret = request.args.get('token')
    if client_secret != SHARED_API_SECRET:
        abort(401, description="Unauthorized: Invalid token")

    # === Fetch videos from your PeerTube channel
    headers = {'Authorization': f'Bearer {PEERTUBE_TOKEN}'}
    url = f'{PEERTUBE_URL}/api/v1/video-channels/{CHANNEL_ID}/videos?page=1&count=50'

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch videos', 'details': response.text}), 500

    videos = response.json().get('data', [])
    video_urls = [f"{PEERTUBE_URL}/w/{v['uuid']}" for v in videos]

    return jsonify(video_urls)

if __name__ == '__main__':
    app.run(port=8080)
