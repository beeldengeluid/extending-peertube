#!/bin/python

import requests, json

headers = {
    'Authorization': 'Bearer fd476f18fb3df5c092302e1fc6518efc3e991764'
}

# files = {
#     'channelId': (None, '2'),
#     'name': (None, 'Test'),
#     'tags[0]': (None, 'tentoon'),
#     'targetUrl': (None, 'https://www.openbeelden.nl/files/11/52/1152271.1152266.WEEKNUMMER481-HRE0000CABE_2369000_2420000.mp4'),
# }

# response = requests.post('https://peertube.beeldengeluid.nl/api/v1/videos/imports', headers=headers, files=files)
# data = response.json()

# print json.dumps(data, indent=2)

data = {
    'channelId': 2,
    'name': 'Test',
    'tags': 'tentoon',
    'targetUrl': 'https://www.openbeelden.nl/files/11/52/1152271.1152266.WEEKNUMMER481-HRE0000CABE_2369000_2420000.mp4'
}

response = requests.post('https://peertube.beeldengeluid.nl/api/v1/videos/imports', headers=headers, data=data)
data = response.json()

print(response.status_code)

print json.dumps(data, indent=2)