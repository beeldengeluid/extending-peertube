#!/usr/bin/python3

import requests
import csv
import json
import time
import os
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

with open('vpro_srt.csv', 'r') as csvfile:
	csv_data = csv.reader(csvfile, delimiter='|')
	for row in csv_data:

		uuid = row[0]
		srt = row[1]

		srt_exists = os.path.exists('data/transcripts/' + srt)

		if srt_exists:
			
			files = {
				'captionfile': (srt, open('data/transcripts/' + srt, 'rb'))
			}

			response = requests.put(api_url + '/videos/' + uuid + '/captions/en', headers=headers, files=files)
			time.sleep(1)

			# print(response)