---
layout: post
title: Updating videos with the API
category: Migration
comments: false
---

After bulk importing videos into a channel you might realize that you have forgotten to set something for all videos or that you made a mistake in setting something. With the help with some Python scripting and the PeerTube API it's possible to bulk update your videos and this article shows how that can be achieved.

<!--more-->

As an example we will show you how we set a category for all videos in a specific channel. The channel that we targeted has the handle 'themindoftheuniverse' and the category is 'Science & Technology' of which the id is 15.

[https://peertube.beeldengeluid.nl/c/themindoftheuniverse](https://peertube.beeldengeluid.nl/c/themindoftheuniverse)
[https://peertube.beeldengeluid.nl/api/v1/videos/categories](https://peertube.beeldengeluid.nl/api/v1/videos/categories)

As we can only return a maximum of 100 videos with the API, we first need to establish the total of the videos in the channel, so we can figure out how many sets of 100 videos we need to update.

```python
channel_handle = 'themindoftheuniverse'

response = requests.get(api_url + '/video-channels/' + channel_handle + '/videos?count=0')
videos = response.json()

total = videos['total']
loops = math.ceil(total/100)
```

Basically this gets the total from making this call to the API without getting the video data (count=0):

https://peertube.beeldengeluid.nl/api/v1/video-channels/themindoftheuniverse/videos?count=0

With the math.ceil function we can calculate how much loops/pages we need to iterate. We start with an offset of zero and then get the next 100 videos by multiplying the iterator `i` with 100.

```python
while i < loops:
	
	offset = i * 100

	# GET videos from channel

	response = requests.get(api_url + '/video-channels/' + channel_handle + '/videos?start=' + str(offset) + '&count=100&skipCount=true')
	videos = response.json()

	for video in videos['data']:

		requests.put(api_url + '/videos/' + video['uuid'], headers=headers, data=data)
		time.sleep(1)

	i += 1
```

For each 100 videos we send a PUT API call to update the video by it's uuid with the data we have defined for category, but it's possible to update several fields at once:

```python
data = {
	'category': 15
}
```

Once again we pause our script for 1 second after each API update call as to not overload the API.
