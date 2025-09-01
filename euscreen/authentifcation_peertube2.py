import requests

# === Configuration ===
PEERTUBE_URL = 'https://peertube.beeldengeluid.nl'
CLIENT_ID = '41vzdcnxkn1ar7q5xitrtg1x3yr725ua'
CLIENT_SECRET = 'bM6jkBTJkL5jmVby3BlJUlXYQuVSocQJ'
USERNAME = 'EUscreen'
PASSWORD = 'Uscream'

TOKEN_URL = f'{PEERTUBE_URL}/api/v1/users/token'

# === Request Access Token with read:video-playlists scope ===
data = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': 'password',
    'username': USERNAME,
    'password': PASSWORD,
    'scope': 'read:video-playlists'#write:videos
}

response = requests.post(TOKEN_URL, data=data)

if response.status_code == 200:
    token_data = response.json()
    print('Access Token:', token_data['access_token'])
    print('Expires In:', token_data['expires_in'], 'seconds')
    print('Scope:', token_data.get('scope', 'Not provided'))
else:
    print('Failed to retrieve token:', response.status_code, response.text)
