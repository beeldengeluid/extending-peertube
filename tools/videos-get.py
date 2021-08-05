#!/usr/bin/python3

import requests

response = requests.get('https://peertube.beeldengeluid.nl/api/v1/videos')
print(response.json())