---
layout: post
title: URL redirection in PeerTube
category: URL-redirection
comments: false
---

With a setup for redirecting a lot of URLs in Nginx by creating several configuration files, in this article we will recommend how to integrate these files in an existing Nginx HTTP server and specifically in PeerTube, which only supports Nginx as a reverse proxy for performance and security.

> The reverse proxy will receive client HTTP requests, and:
>
> * Proxy them to the API server
> * Serve requested static files (Video files, stylesheets, javascript, fonts...)

So we extend this with another functionality:

* redirect old URls from a video website to the PeerTube URLs

<!--more-->

Nginx keeps it's configuration in the expected `/etc/nginx` directory. This directory is broken up as can be seen on the [Debian wiki page](https://wiki.debian.org/Nginx/DirectoryStructure).

As we can see from the description of this directory structure, the default nginx.conf file includes a line that will load additional configurations files into the http { } context from `/etc/nginx/conf.d/`. This is where we drop in the global mapping directive as a file called `redirect.conf`, although any other filename will work the same:

```
map_hash_max_size 8192;
map_hash_bucket_size 128;

map $request_uri $old_id {
  ~^/media/([0-9]+) $1;
}

map $old_id $new_id {
  include /etc/nginx/snippets/rewritemap.conf;
}
```

In this file we include the configuration snippet file `rewritemap.conf` from the directory `/etc/nginx/snippets/`. This is the big file with the old ids and new ids that looks like this (first 10 lines):

```
1215870 35d6b543-d830-4678-a7f1-fda30c0ec95d;
1193100 4d76aaa4-a991-444d-a282-42e2cebf5912;
1216245 cebe1695-a289-4698-8a95-1efaaf9f13fd;
1216823 ec131ab0-429a-444c-b262-18dd6a1a57b8;
1216986 6196ddec-f7b7-454e-89e6-9d29740db259;
1216173 7e8b8069-4897-4db1-875c-199a62b2e279;
1215985 4b28ce84-7a33-46d5-964c-e315518e48ba;
1216848 b889fa83-d860-4d57-9e23-de76f2fdc688;
1196886 bccaa3b0-3baf-4ece-9afa-e0347a66dc0d;
1196956 a94c4000-1ee1-4bf6-bac2-40e5e05029f3;
```

Now there are 2 ways to integrate the redirects in PeerTube, depending on if you want to redirect URLs from an old domain name to the new one of your PeerTube instance, or if you keep the old domain name.

If you migrate from an old domain name, you can create a seperate configuration file for that specific server_name when you point this domain name to the same IP as the PeerTube instance by changing it's DNS record. This file can be dropped into `/etc/nginx/conf.d/` as well to have it automatically loaded or you could use the usual `/etc/nginx/sites-available/` and `/etc/nginx/sites-enabled/` structure for defining virtual hosts.

In our example we could name the file `openbeelden.conf` to refer to the old domain name `openbeelden.nl`.

```
server {
  listen 80;
  listen [::]:80;
  listen 443 ssl http2;
  listen [::]:443 ssl http2;

  server_name openbeelden.nl;

  if ($new_id) {
    return 301 https://peertube.beeldengeluid.nl/videos/watch/$new_id;
  }

  return 301 https://peertube.beeldengeluid.nl$request_uri;
}
```

As you can see from the last line, we will also redirect old URLs to our new domain that didn't match a video web page, including the part that was requested with $request_uri. This means that other URLs like https://www.openbeelden.nl/about will be redirected to https://peertube.beeldengeluid.nl/about if it exists or not. If you don't want this to result in possible 404 "Not found" responses, you could leave out the $request_uri part and let the user land on your PeerTube home page.

In the case that you keep your old domain name, which will be the same domain name as for your PeerTube server, then you will have to edit the existing `/etc/nginx/sites-available/peertube` file that was created during the install of PeerTube in the part about [Webserver in the production guide](https://github.com/Chocobozzz/PeerTube/blob/develop/support/doc/production.md#webserver). By editing this file you can add the `if` statement, just after the 'Application' comment.

```
server {

  # ...

  ##
  # Application
  ##

  if ($new_id) {
    return 301 /videos/watch/$new_id;
  }

  # ...

}
```

We have tested this second setup with our own instance where we haven't migrated from an old domain name. With the example we have used before, you can see how you get properly redirected by following this link:

[https://peertube.beeldengeluid.nl/media/1000452](https://peertube.beeldengeluid.nl/media/1000452)

It shows the same video with the new PeerTube URL as on the page where we have imported the video from:

[https://www.openbeelden.nl/media/1000452](https://www.openbeelden.nl/media/1000452)

Either way, after implementing this added Nginx configuration, you only have to reload Nginx to activate your URL-redirection solution:

```sh
$ sudo systemctl reload nginx
```

If you want to implement your own URL redirection for Nginx, we have added all files as examples/templates to our Github repository in our 'tools' folder, which can be found at:

[https://github.com/beeldengeluid/extending-peertube/tree/main/tools/nginx](https://github.com/beeldengeluid/extending-peertube/tree/main/tools/nginx)

