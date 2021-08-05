---
layout: post
title: Importing videos with the API
category: Migration
comments: false
---

To upload or import a video with the API to your PeerTube instance, it only requires 3 pieces of data:

* a video source file (either by file upload or by target URL import)
* a title for the video (between 3 and 120 characters)
* a channel ID that will contain the video (number 1 or higher)

There are a lot of other optional data fields you can set and in this post we will show how we imported videos in bulk with their metadata.

<!--more-->

Before you start uploading videos, you first have to know the required channelID of the channel that will contain the videos. Once you have created a channel through the PeerTube interface (or have a default main channel after signup), you can find the channel ID by listing the channels with the API:

[https://peertube.beeldengeluid.nl/api/v1/video-channels](https://peertube.beeldengeluid.nl/api/v1/video-channels)

As we were targeting our channel named 'openbeelden', we found that the channelID is 2.

To understand what other data can be added to our video imports, it's important to look first what the options and/or restrictions are to the data. In the [PeerTube REST API documentation](https://docs.joinpeertube.org/api-rest-reference.html#operation/importVideo) it's described in relatively easy to understand OpenAPI format.

As we exported data for around 7000 videos in a big CSV file, we first had to map the data to something that would fit the PeerTube data model. This is an example of 1 line/record in our data file:

```
oai:openimages.eu:1215870|"Het gerestaureerde carillon speelt weer"||carillons;gemeentehuizen;klokken|"Weekjournaal van Polygoon Hollands Nieuws van week 27 uit 1949."|"Het gerestaureerde carillon van de stadhuistoren in Veere wordt opnieuw in gebruik genomen. De stadsbeiaardier van Rotterdam, Ferdinand Timmermans, speelt oa het Zeeuwse volkslied. SHOTS: - stadsshots en straatshots; - ext. stadhuis; op het bordes luisteren de burgemeester en gezelschap; - int. stadhuistoren; beiaard en beiaardier; - enkele shots van luisterend publiek dat grotendeels bestaat uit mensen in Zeeuwse klederdracht."|"Polygoon Hollands Nieuws (producent) / Nederlands Instituut voor Beeld en Geluid (beheerder)"|1949-06-27|https://www.openbeelden.nl/media/1215870|https://creativecommons.org/publicdomain/mark/1.0/|https://www.openbeelden.nl/files/12/15/1217877.1215874.WEEKNUMMER492-HRE000132B4_2551000_2626960.mp4|https://www.openbeelden.nl/files/12/15/1217883.1215874.WEEKNUMMER492-HRE000132B4_2551000_2626960.ogv
```

First we defined a text cap funtion to prevent failed imports due to too long text items and a dictionairy to map the licence links in our data to the PeerTube licence IDs (see: https://peertube.beeldengeluid.nl/api/v1/videos/licences)

```python
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
```

Next we open 3 files we need during import: the data source CSV file ('openbeelden.csv'), an empty CSV file (named 'delta.csv') where we add the records that fail during import and another file ('rewritemap.conf') where we add the old video id and the new video id after import to later create an URL redirect map.

```python
file_delta = open('data/delta.csv', 'a', newline='')
delta_writer = csv.writer(file_delta, delimiter='|')

file_rewritemap = open('rewritemap.conf', 'a')

with open('data/openbeelden.csv', 'r') as csvfile:
	csv_data = csv.reader(csvfile, delimiter='|')
	for row in csv_data:
```

While looping to all the rows/lines in our data file, we match the field by their index number (0 for first field), strip unnecessary spaces and put them in named variables for further processing:

```python
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
```

The following steps transforms this data so it's acceptable for import. We cap the texts to their maximum, get the licence id and restrict the tags to 5 unique items that are between 2 and 30 characters long. We also combine descriptive texts from our data to 1 extended description.

```python

title = cap(title, 120)

licence = licence_links.get(licence_link, '')

tags = list(dict.fromkeys(tags))
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
```

Next we prepare our transformed data and post it to the video import API endpoint. Some data like language (nl) and privacy (1 = public) and booleans for commentsEnabled and downloadEnabled we set fixed for all videos:

```python
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
```

By checking if the import succeeds or fails we either write the old and new id to our rewritemap file or we add the failed record to our delta file:

```python
if response.status_code == requests.codes.ok:

	data = response.json()
	uuid = data['video']['uuid']

	file_rewritemap.write(old_id + " " + uuid + ";\r\n")

else:

	delta_writer.writerow(row

time.sleep(1)
```

We end this iteration of the loop with a 1 second pause as to prevent that we overflow the API with too many concurrent requests.

Once we were done with importing the videos we checked our delta file for failed imports and adjusted the data accordingly so we could use this file for another import. 

Only recently (since version 3.3) the error responses have been normalized in PeerTube, so it might be wise to add this error response text as another field to the delta file to get a clear indication of why the import fails. 