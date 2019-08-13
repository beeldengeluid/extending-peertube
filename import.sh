#!/bin/bash

# function test {
#   echo Column 1: $1
#   echo Column 2: $2
# }
# export -f test
# csvtool -t '|' call test openbeelden.csv

# csvtool -t '|' openbeelden.csv

testfunction() {
  echo column one is "$1"
}

export -f testfunction
echo one,two,three | csvtool call testfunction -

exit;

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
USERNAME="nisv"
PASSWORD="openbeelden"

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





# function strip_quotes() {
# 	string=$s1
# 	# string=${string#"\""}
# 	# string=${string%"\""}
# 	echo $1
# }

# while IFS='|' read -r f1 f2 f3 f4 f5 f6 f7
# do
# 	title=$f2
# 	title=${title#"\""}
# 	title=${title%"\""}
#   echo $title
# done < openbeelden.csv



# client_secret=$(http -b GET "$API_PATH/oauth-clients/local" | jq -r ".client_secret")
# token=$(http -b --form POST "$API_PATH/users/token" \
#   client_id="$client_id" client_secret="$client_secret" grant_type=password response_type=code \
#   username=$USERNAME \
#   password=$PASSWORD \
#   | jq -r ".access_token")
# ## VIDEO UPLOAD
# http -b --form POST "$API_PATH/videos/upload" \
#   videofile@$FILE_PATH \
#   channelId=$CHANNEL_ID \
#   name=$NAME \
#   "Authorization:Bearer $token"