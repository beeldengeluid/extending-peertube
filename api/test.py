#!/bin/python

import requests, json

# API vars

api_url = 'https://peertube.beeldengeluid.nl/api/v1'
api_user = 'root'
api_pass = 'tazifosemigefuki'

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

response = requests.get(api_url + '/jobs/failed?count=1', headers=headers)
data = response.json()

print json.dumps(data, indent=2)

# files = {
#     'channelId': (None, '2'),
#     'name': (None, 'TestYYY'),
#     'commentsEnabled': (None, '0'),
#     'downloadEnabled': (None, '0'),
#     'targetUrl': (None, 'https://www.openbeelden.nl/files/11/52/1152271.1152266.WEEKNUMMER481-HRE0000CABE_2369000_2420000.mp4'),
# }

# response = requests.post(api_url + '/videos/imports', headers=headers, files=files)
# data = response.json()

# print json.dumps(data, indent=2)

# data = {
#     'channelId': '2',
#     'name': 'TestDisabled2',
#     'commentsEnabled': False,
#     'downloadEnabled': False,
#     'targetUrl': 'https://www.openbeelden.nl/files/11/52/1152271.1152266.WEEKNUMMER481-HRE0000CABE_2369000_2420000.mp4'
# }

# response = requests.post(api_url + '/videos/imports', headers=headers, data=data)
# data = response.json()

# print(response.status_code)

# print json.dumps(data, indent=2)

