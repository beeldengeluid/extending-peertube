---
layout: post
title: Using the PeerTube API with Python
category: Tools
comments: false
---

The PeerTube API is built on HTTP(S) and is RESTful. You can use your favorite HTTP/REST library for your programming language to use PeerTube. See the [REST API quick start](https://docs.joinpeertube.org/api-rest-getting-started) for a few examples of using the PeerTube API. For the sake of simplicity we are using Python and this article is a short introduction to some of the basic concepts of our Python tools/scripts.

<!--more-->

As one of the examples of using the PeerTube API, you can make an HTTP(S) GET request to the `/api/v1/videos` endpoint. As you can see by following the link 

[https://peertube.beeldengeluid.nl/api/v1/videos](https://peertube.beeldengeluid.nl/api/v1/videos) 

in your browser this will return data of the videos in JSON.

[Requests](https://en.wikipedia.org/wiki/Requests_(software)) is also the name of a popular HTTP library for the Python programming language. This library is thus essential and imported as first in the header of our scripts.

```python
#!/usr/bin/python3

import requests
```

With this library we can retrieve the same data as above by sending a GET request and outpout the response:

```python
response = requests.get('https://peertube.beeldengeluid.nl/api/v1/videos')
print(response.json())
```

For a lot of things you can do with the PeerTube API (like create, update or delete a video), you need to be authorized and therefore authenticated first. When you sign up for an account on a PeerTube instance, you are given the possibility to generate sessions on it, and authenticate there using an access token.

Authenticating via OAuth requires the following steps:

* Have an activated account
* Generate an access token for that account at `/api/v1/users/token`.
* Make requests with the *Authorization: Bearer <token>* header

This is how we implement these steps. First we define our activated account (api_pass is the password of the account):

```python
api_url = 'https://peertube.beeldengeluid.nl/api/v1'
api_user = 'nisv'
api_pass = 'xxxxxxxxxxxx'
```

Then we get the OAuth client token with the help of the requests library: 

```python
response = requests.get(api_url + '/oauth-clients/local')
data = response.json()
client_id = data['client_id']
client_secret = data['client_secret']
```

Now we can fetch the user access token by sending the client token with our username and password:

```python
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
```

With the access token we can define the headers that we will use with our requests:

```python
headers = {
	'Authorization': token_type + ' ' + access_token
}
```

For example this will look something like this when we want to update a video in our script with a PUT action on the `/api/v1/videos` API endpoint:

```python
requests.put(api_url + '/videos/sY6rPiwzy85rQxwp1E7LMa', headers=headers, data=data)
```

Being able to make authorized requests in this way, opens up a lot of functionality to do things programmatically through the API that are not possible in the web interface of PeerTube, like bulk importing and/or updating videos.
