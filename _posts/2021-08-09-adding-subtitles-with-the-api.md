---
layout: post
title: Adding subtitles with the API
category: Subtitles
comments: false
---

Adding subtitles or captions to a video in PeerTube is done after uploading/importing a video. As the subtitles of the video need to be in a  text-based file (either a `.srt` or `.vtt` file) it will be uploaded separately and transformed in a WebVTT (`.vtt`) format so it can be used in the video player. In this article we will show how to bulk upload existing subtitle files with the PeerTube API.

<!--more-->

As an example we will show you how we added existing subtitle files for most videos in the 'themindoftheuniverse' channel with the use of the [Video Captions endpoint of the API](https://docs.joinpeertube.org/api-rest-reference.html#tag/Video-Captions). 

For adding subtitle we need 3 pieces of data:

* the identifier of the video (the object id, uuid or short uuid)
* the subtitle file (captionFile as `.srt` or `.vtt`)
* the language of the subtitle file (captionLanguage in short, like `en`)

As we have shown in the article on [bulk importing videos](https://beeldengeluid.github.io/extending-peertube/migration/2021/07/06/importing-videos-with-the-api.html), you only know the identifier of the video after it has been assigned by a succesful upload/import. This means you could add the subtitle file right after this part in the video-imports script when you collect the uuid from the response:

```python
if response.status_code == requests.codes.ok:

    data = response.json()
    uuid = data['video']['uuid']
```

If you generate subtitles after upload/import, it's important to find a way to couple the video identifier with the subtitle file if you want to bulk upload your subtitle files as well. For instance, you could give your subtitle file the same name as the identifier (like 192727.srt if you use the object id as identifier). In our case we generated a small csv file to 'map' the video uuid with the subtitle file like below (first 10 records):

```csv=
5a71eb42-d31d-4cf0-9a63-42319bfeb9c6|Guy_Consolmagno__ex2.srt
0721c557-b4d9-4ef9-ad97-91d663b38125|Yuri_Oganessian__ex2.srt
9f1b6821-a930-4653-b400-c1f517da7da6|Carolina_Cruz__br.srt
b6d136c8-dd4d-4792-97ec-979f27a7d833|Artur_Avila__br.srt
1ab7edd6-a41a-451e-946c-cfb2b97947e7|Joanna_Aizenberg.srt
0c53e6c5-9890-4696-88b6-7d3246405ce5|Pascale_Fung.srt
1fddd827-d868-4f1e-b649-ff8a2893dae6|Susant_Pattnaik__ex2.srt
cd1fbc56-110c-4243-80a5-f36aa3082840|Lee_Cronin__ex2.srt
7a66ecd9-f5e1-4638-a62c-26532c804632|Lee_Cronin__ex.srt
28ad638d-a795-459c-9f1e-4775a5174cec|George_Church__ex.srt
```

This file is then used by reading it line by line and adding a subtitle file through the API:

```python
with open('data/vpro_srt.csv', 'r') as csvfile:
    csv_data = csv.reader(csvfile, delimiter='|')
	for row in csv_data:

        uuid = row[0]
		srt = row[1]

		srt_exists = os.path.exists('data/transcripts/' + srt)

		if srt_exists:
			
			files = {
				'captionfile': (srt, open('data/transcripts/' + srt, 'rb'))
			}

			response = requests.put(api_url + '/videos/' + uuid + '/captions/en', headers=headers, files=files)
			time.sleep(1)
```

As you can see from the PUT request it either adds a subtitle file for the language specified in the API url (`/captions/en`) or replaces the subtitle file for that language if there is a pre-existing file.

Generating subtitle files is mostly something that's been done in post-production of a video and there is still a lot of development in (semi-)automatic subtitling (by ASR, Automatic Speech Recognition, for instance) and it's not as advanced for all natural languages, but in a future article we will suggest some recommendations for tools/solutions in this domain.
