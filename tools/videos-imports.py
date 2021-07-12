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

# NOTE: there are only 7 default licenses in PeerTube. For any number above that you need a plugin which adds more license options
# https://github.com/beeldengeluid/peertube-plugin-creative-commons

licence_links = {
	'https://creativecommons.org/licenses/by/3.0/nl/': '1',
	'https://creativecommons.org/licenses/by-sa/3.0/nl/': '2',
	'https://creativecommons.org/licenses/by-nd/3.0/nl/': '3',
	'https://creativecommons.org/licenses/by-nc/3.0/nl/': '4',
	'https://creativecommons.org/licenses/by-nc-sa/3.0/nl/': '5',
	'https://creativecommons.org/licenses/by-nc-nd/3.0/nl/': '6',
	'https://creativecommons.org/publicdomain/zero/1.0/': '7',
	'https://creativecommons.org/publicdomain/mark/1.0/': '8' 
}

i = 1

file_delta = open('delta.csv', 'a', newline='')
delta_writer = csv.writer(file_delta, delimiter='|')

file_rewritemap = open('rewritemap.conf', 'a')

with open('openbeelden.csv', 'r') as csvfile:
	csv_data = csv.reader(csvfile, delimiter='|')
	for row in csv_data:

		time.sleep(2)

		# Clean data

		uri = row[0].split(':');
		old_id = uri[2];
		title = row[1].strip()
		alternative = row[2].strip()
		tags = row[3].split(';');
		description = row[4].strip()
		abstract = row[5].strip()
		creator = row[6].strip()
		date = row[7].strip()
		url_old = row[8].strip()
		licence_link = row[9].strip()
		video = row[10].strip() # mp4 HD

		if not video:
			video = row[11].strip() # ogv HD

		# Transform data
		# https://github.com/Chocobozzz/PeerTube/blob/develop/server/initializers/constants.ts

		title = cap(title, 120)

		licence = licence_links.get(licence_link, '')

		tags = list(filter(lambda a: len(a) >= 2, tags))
		tags = list(filter(lambda a: len(a) <= 30, tags))
		tags = tags[:5]

		description_ext = ''

		if alternative:
			description_ext += alternative + '\n\n'

		if description:
			description_ext += description + '\n\n'

		if abstract:
			description_ext += abstract + '\n\n'

		description_ext = cap(description_ext, 9800)

		if creator:
			description_ext += creator

		# Import video, use multipart/form-data request with 'files'

		data = {
			'name': (None, title),
			'channelId': (None, str(channel_id)),
			'targetUrl': (None, video),
			'language': (None, 'nl'),
			'privacy': (None, '1'),
			'commentsEnabled': (None, 'false'),
			'downloadEnabled': (None, 'true'),
			'description': (None, description_ext),
			'originallyPublishedAt': (None, date)
		}

		# create indexed array for tags

		for j in range(len(tags)):
			data['tags[' + str(j) +']'] = (None, tags[j])

		if licence:
			data['licence'] = (None, licence)

		response = requests.post(api_url + '/videos/imports', headers=headers, files=data)

		if response.status_code == requests.codes.ok:

			data = response.json()
			uuid = data['video']['uuid']

			file_rewritemap.write(old_id + " " + uuid + ";\r\n")

			# print(json.dumps(data, indent=2))

		else:

			delta_writer.writerow(row)

			# error = response.json()

			# print(json.dumps(error, indent=2))

		i += 1

file_rewritemap.close()
file_delta.close()