#!/bin/bash

## DEPENDENCIES: jq
USERNAME="nisv"
PASSWORD="xxx"
FILE_PATH="/mnt/share/PONTONNIERS_S-FHD00Z01ZMW_480880_664200.mp4"
CHANNEL_ID="2"
NAME="Pontonniers slaan brug over de Rijn"
API="https://peertube.beeldengeluid.nl/api/v1"

## AUTH
client_id=$(curl -s "$API/oauth-clients/local" | jq -r ".client_id")
client_secret=$(curl -s "$API/oauth-clients/local" | jq -r ".client_secret")
token=$(curl -s "$API/users/token" \
  --data client_id="$client_id" \
  --data client_secret="$client_secret" \
  --data grant_type=password \
  --data username="$USERNAME" \
  --data password="$PASSWORD" \
  | jq -r ".access_token")

## VIDEO UPLOAD
curl -s "$API/videos/upload" \
  -H "Authorization: Bearer $token" \
  --max-time 600 \
  --form videofile=@"$FILE_PATH" \
  --form channelId=$CHANNEL_ID \
  --form name="$NAME"