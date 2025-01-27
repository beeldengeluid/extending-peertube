#!/usr/bin/python3

import requests
import json
import math
import time
import configapi as cfg

# API vars (from configapi.py)

# api_url = 'https://peertube.beeldengeluid.nl/api/v1'
# api_user = 'nisv'
# api_pass = 'xxxxxxxxxxxx'

api_url = cfg.api_url
api_user = cfg.api_user
api_pass = cfg.api_pass

channel_handle = 'afp'

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
	'downloadEnabled': 'True'
}

# GET videos total from channel

response = requests.get(api_url + '/video-channels/' + channel_handle + '/videos?count=0')
videos = response.json()

total = videos['total']
loops = math.ceil(total/100)

i = 0

while i < loops:
	
	offset = i * 100

	# GET videos from channel

	response = requests.get(api_url + '/video-channels/' + channel_handle + '/videos?start=' + str(offset) + '&count=100&skipCount=true')
	videos = response.json()

	for video in videos['data']:

		requests.put(api_url + '/videos/' + video['uuid'], headers=headers, data=data)
		time.sleep(1)

	i += 1
