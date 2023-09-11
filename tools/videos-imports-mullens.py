#!/usr/bin/python3

import requests
import csv
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

# Import Openbeelden videos

def cap(text, length):
	return text if len(text) <= length else text[0:length-3] + '...'

file_delta = open('data/delta.csv', 'a', newline='')
delta_writer = csv.writer(file_delta, delimiter='|')

file_rewritemap = open('rewritemap.conf', 'a')

row_nr = 0

with open('data/mullens.csv', 'r') as csvfile:
	csv_data = csv.reader(csvfile, delimiter=';')
	for row in csv_data:

		row_nr += 1

		if (row_nr > 0 and row_nr <= 368):

			# Clean data

			video = row[0].strip() # mp4 HD
			old_id = row[1].strip()
			title = row[2].strip()
			creator = row[3].strip()
			licence = row[4].strip() # PDM 
			language = row[5].strip()
			date = row[6].strip()
			tags = row[7].split(';');
			location = row[8].split(';');
			description = row[9].strip()

			# Transform data
			# https://github.com/Chocobozzz/PeerTube/blob/develop/server/initializers/constants.ts

			title = cap(title, 120)

			tags = list(dict.fromkeys(tags))
			tags = list(filter(lambda a: len(a) >= 2, tags))
			tags = list(filter(lambda a: len(a) <= 30, tags))
			tags = tags[:5]

			description_ext = ''

			if description:
				description_ext += description + '\n\n'

			description_ext = cap(description_ext, 9800)

			if creator:
				description_ext += creator

			# Import video, use multipart/form-data request with 'files'

			videofile = "/mnt/share/Flipfactory/voor_Johannes/Openbeelden/" + video

			# files = {'file': ('report.xls', open('report.xls', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}

			data = {
				'videofile': (video, open(videofile ,'rb'), 'video/mp4'),
				'name': (None, title),
				'channelId': (None, str(channel_id)),
				'language': (None, 'nl'),
				'privacy': (None, '1'),
				'commentsEnabled': (None, 'false'),
				'downloadEnabled': (None, 'true'),
				'description': (None, description_ext),
				'licence': (None, '8')
			}

			if date:
				data['originallyPublishedAt'] = (None, date)

			# create indexed array for tags

			for j in range(len(tags)):
				data['tags[' + str(j) +']'] = (None, tags[j])

			# print(data)
			# quit()

			response = requests.post(api_url + '/videos/upload', headers=headers, files=data, timeout=600)

			if response.status_code == requests.codes.ok:

				data = response.json()
				uuid = data['video']['uuid']

				file_rewritemap.write(old_id + " " + uuid + ";\r\n")

				print("Row number: " + str(row_nr))

				print(json.dumps(data, indent=2))

			else:

				print(response.status_code)
				print(response.reason)
				print(response.content)

				delta_writer.writerow(row)

				# error = response.json()

				# print(json.dumps(error, indent=2))

			time.sleep(1)

file_rewritemap.close()
file_delta.close()