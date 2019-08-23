#!/bin/bash

# Check dependencies

if ! command curl --version > /dev/null 2>&1 ; then
	echo "This script uses curl, see the online docs at https://curl.haxx.se/"
	exit
fi

if ! command jq --version > /dev/null 2>&1 ; then
	echo "This script uses jq, see the online docs at https://stedolan.github.io/jq"
	exit
fi

API_PATH="https://peertube.beeldengeluid.nl/api/v1"
USERNAME="root"
PASSWORD="tazifosemigefuki"

# Get client

json_response=$(curl -s "$API_PATH/oauth-clients/local")
client_id=$(echo $json_response | jq -r ".client_id")
client_secret=$(echo $json_response | jq -r ".client_secret")

# Get token

post_vars="client_id=$client_id&"
post_vars+="client_secret=$client_secret&"
post_vars+="grant_type=password&"
post_vars+="response_type=code&"
post_vars+="username=$USERNAME&"
post_vars+="password=$PASSWORD"

json_response=$(curl -s -X POST -d "$post_vars" "$API_PATH/users/token")
token=$(echo $json_response | jq -r ".access_token")

# Authorization

auth_header="Authorization: Bearer $token"

#
# Testing playground
#

# Test PUT date

# uuid=a2df9503-5575-44d2-8423-dc578228100b
# post_vars="originallyPublishedAt=2015-11-29"
# curl -s -H "$auth_header" -X PUT -d "$post_vars" "$API_PATH/videos/$uuid"

# Test GET config

# curl -H "$auth_header" "$API_PATH/config/custom" | jq


# Test POST tags

echo curl -H "$auth_header" -X POST \
-F "channelId=2" \
-F "name=Test" \
-F "tags[0]=tentoon" \
-F "targetUrl=https://www.openbeelden.nl/files/11/52/1152271.1152266.WEEKNUMMER481-HRE0000CABE_2369000_2420000.mp4" \
"$API_PATH/videos/imports"