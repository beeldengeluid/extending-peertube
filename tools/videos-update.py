#!/usr/bin/python3

import requests
import json
import time
import configapi as cfg

# API vars (from configapi.py)

# api_url = 'https://peertube.beeldengeluid.nl/api/v1'
# api_user = 'nisv'
# api_pass = 'xxxxxxxxxxxx'
# channel_id = 2

api_url = cfg.api_url
api_user = cfg.api_user
api_pass = cfg.api_pass
channel_id = cfg.channel_id

# Get client

response = requests.get(api_url + '/oauth-clients/local')
data = response.json()
client_id = data['client_id']
client_secret = data['client_secret']

# Get user token

data = {
	'client_id': client_id,
	'client_secret': client_secret,
	'grant_type': 'password',
	'response_type': 'code',
	'username': api_user,
	'password': api_pass
}

response = requests.post(api_url + '/users/token', data=data)
data = response.json()
token_type = data['token_type']
access_token = data['access_token']

# Authorization header

headers = {
	'Authorization': token_type + ' ' + access_token
}

# Update this data

data = {
	'downloadEnabled': 'true'
}

# GET videos from channel: https://peertube.beeldengeluid.nl/api/v1/video-channels/openbeelden/videos

i = 1

while i <= 35:

	offset = i * 100

	print(offset)

	response = requests.get(api_url + '/video-channels/openbeelden/videos?start=' + str(offset) + '&count=100')
	videos = response.json()

	for element in videos['data']:

		time.sleep(2)

		response = requests.get(api_url +'/videos/' + element['uuid'])
		video = response.json()

		if bool(video['downloadEnabled']):

			print('true: ' + video['uuid'])

		else:

			print('false: ' + video['uuid'])
			
			requests.put(api_url + '/videos/' + video['uuid'], headers=headers, data=data)

	i += 1