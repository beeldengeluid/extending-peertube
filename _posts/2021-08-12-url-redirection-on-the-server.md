---
layout: post
title: URL redirection on the server
category: URL-redirection
comments: false
---

URL redirection, also called URL forwarding, is a World Wide Web technique for making a web page available under more than one URL address. When a web browser attempts to open a URL that has been redirected, a page with a different URL is opened.

URL redirection is done for various reasons:

* for URL shortening;
* to prevent broken links when web pages are moved;
* to allow multiple domain names belonging to the same owner to refer to a single web site;
* to guide navigation into and out of a website;
* for privacy protection; and
* for hostile purposes such as phishing attacks or malware distribution.

> from Wikipedia: [URL redirection](https://en.wikipedia.org/wiki/URL_redirection)

In our case we focus on the second reason: to prevent broken links after migrating a video streaming website to PeerTube.

<!--more-->

Several different kinds of response to the browser will result in a redirection. These vary in whether they affect HTTP headers or HTML content. The techniques used typically depend on the role of the person implementing it and their access to different parts of the system. For example, a web author with no control over the headers might use a Refresh meta tag whereas a web server administrator redirecting all pages on a site is more likely to use server configuration.

We will focus on the implementation of redirects in a server configuration, for which we need to send a HTTP header with the status code 301 to specify the URL is "moved permanently".

For instance if we want to redirect this video web page URL:

`https://www.openbeelden.nl/media/1000452`

to our new PeerTube web page:

`https://peertube.beeldengeluid.nl/videos/watch/b0fd82cf-68b7-447d-a5fe-ed5706cd991a`

In a configuration for Apache HTTP Server this would be implemented like:

```
<VirtualHost *:80>
    ServerName www.openbeelden.nl
    Redirect 301 /media/1000452 https://peertube.beeldengeluid.nl/videos/watch/b0fd82cf-68b7-447d-a5fe-ed5706cd991a
</VirtualHost>
```

There are also some other ways to achieve the same and the documentation on  Redirecting and Remapping for the [Apache HTTP Server](https://httpd.apache.org/docs/2.4/rewrite/remapping.html) is extensive and of very high quality. For the nginx webserver all this can be done in a very similar matter, but it's documentation is a bit more sparse.

Adding redirects like this (by adding a Redirect directive for every page) to a webserver configuration works perfectly fine if you only want to redirect several pages, but runs into a problem with scale. 

To understand this you have to think about what happens if you have a couple of hundred, thousand or even tens of thousands of redirects. For every request to the webserver it will try to match all redirect directives line for line, which will have an impact on the time the webserver responds.

Fortunately webservers have a way to do a fast lookup of a key-value pairs by using so-called mapping files which will be loaded in memory/cache.

With a text file that looks like this:

```
##
## rewritemap.txt - old ID to new ID map file
##

1215870 35d6b543-d830-4678-a7f1-fda30c0ec95d
1193100 4d76aaa4-a991-444d-a282-42e2cebf5912
1216245 cebe1695-a289-4698-8a95-1efaaf9f13fd
1216823 ec131ab0-429a-444c-b262-18dd6a1a57b8
1216986 6196ddec-f7b7-454e-89e6-9d29740db259
1216173 7e8b8069-4897-4db1-875c-199a62b2e279
1215985 4b28ce84-7a33-46d5-964c-e315518e48ba
1216848 b889fa83-d860-4d57-9e23-de76f2fdc688
1196886 bccaa3b0-3baf-4ece-9afa-e0347a66dc0d
1196956 a94c4000-1ee1-4bf6-bac2-40e5e05029f3
```

you could implement a solution like this with [RewriteMap](https://httpd.apache.org/docs/2.4/rewrite/rewritemap.html) for the Apache HTTP Server:

```
RewriteMap old2newid "txt:/etc/apache2/rewritemap.txt"
```

```
RewriteEngine on
RewriteRule "^/media/(.*)" "/videos/watch/${old2newid:$1}" [PT]
```

Note: The RewriteMap directive may not be used in <Directory> sections or .htaccess files. You must declare the map in server or virtualhost context. You may use the map, once created, in your RewriteRule and RewriteCond directives in those scopes. You just can't __declare__ it in those scopes.

After some searching we found that you can do the same with nginx, although it's slightly more tricky to get it right. In a next article we will show how to set this up for nginx and how we integrated it in the [PeerTube architecture](https://docs.joinpeertube.org/contribute-architecture?id=technical-overview).
