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

# Import Amateurfilms videos

def cap(text, length):
	return text if len(text) <= length else text[0:length-3] + '...'

# file_delta = open('data/delta.csv', 'a', newline='')
# delta_writer = csv.writer(file_delta, delimiter='|')

# file_rewritemap = open('rewritemap.conf', 'a')

row_nr = 0

with open('data/clement.csv', 'r') as csvfile:
	csv_data = csv.reader(csvfile, delimiter=',')
	for row in csv_data:

		row_nr += 1

		if (row_nr > 1 and row_nr <= 50):

			# Clean data

			collection = row[0].strip()
			video = row[1].strip() # MXF
			title = row[2].strip()
			# daan_link = row[3].strip()
			# daan_id = row[4].strip()

			tags = row[6].split(';');
			location = row[7].strip();
			description = row[8].strip()
			pgm = row[9].strip() 
			date = row[10].strip()
			description_shots = row[11].strip()

			video = video.replace('.mxf','.mp4')

			# Transform data
			# https://github.com/Chocobozzz/PeerTube/blob/develop/server/initializers/constants.ts

			title = cap(title, 120)

			tags = list(dict.fromkeys(tags))
			tags = list(filter(lambda a: len(a) >= 2, tags))
			tags = list(filter(lambda a: len(a) <= 30, tags))
			tags = tags[:5]

			description_ext = ''

			daan_md = 'Bron: [URN:NBN:NL:IN:20-' + pgm + '](https://persistent-identifier.nl/?identifier=URN:NBN:NL:IN:20-' + pgm + ')'

			description_ext += daan_md + '\n\n'

			if description:
				description_ext += description + '\n\n'

			if description_shots:
				description_ext += description_shots + '\n\n'

			description_ext += 'Collectie: ' + collection + '\n'
			description_ext += 'Locatie: ' + location + '\n'


			# description_ext = cap(description_ext, 9800)

			# Import video, use multipart/form-data request with 'files'

			videofile = r"/mnt/share/DaD/Digitaal_Acquisitie_Depot/PDM amateurfilms (peertube)/Clement/" + video

			# files = {'file': ('report.xls', open('report.xls', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}

			data = {
				'videofile': (video, open(videofile ,'rb'), 'video/mp4'),
				'category': (None, '6'),
				'name': (None, title),
				'channelId': (None, str(channel_id)),
				'language': (None, 'nl'),
				'privacy': (None, '1'),
				'commentsEnabled': (None, 'false'),
				'downloadEnabled': (None, 'false'),
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

				#file_rewritemap.write(old_id + " " + uuid + ";\r\n")

				print("Row number: " + str(row_nr))

				print(json.dumps(data, indent=2))

			else:

				print(response.status_code)
				print(response.reason)
				print(response.content)

				# delta_writer.writerow(row)

				# error = response.json()

				# print(json.dumps(error, indent=2))

			time.sleep(1)

#file_rewritemap.close()
# file_delta.close()