---
layout: post
title: URL mapping with Nginx
category: URL-redirection
comments: false
---

Nginx’s map module lets you create variables in Nginx’s configuration file whose values are conditional — that is, they depend on other variables’ values. In this guide, we will look at how to use Nginx’s map module to implement redirects from old website URLs to new ones.

<!--more-->

For small websites with only a few pages, simple if conditional statements can be used for redirects and similar things. However, such a configuration is not easy to maintain or extend in the long run as the list of conditions grows longer.

The map module is a core Nginx module, which means it doesn’t need to be installed separately. It allows you to compare Nginx variable values against a list of conditions and then associate a new value with the variable depending on the match.

To create the necessary map and redirect configuration, we adapt a Nginx configuration file (for instance `/etc/nginx/sites-available/default`):

```
. . .
# Default server configuration
#

# Old website redirect map
#
map $uri $new_uri {
    /old.html /index.html;
}

server {
    listen 80 default_server;
    listen [::]:80 default_server;

    # Old website redirect
    if ($new_uri) {
        rewrite ^ $new_uri permanent;
    }
. . .
```
The section before the `server` block is a new `map` block, which defines the mapping between the old URLs and the new ones using the map module. The section inside the `server` block is the redirect itself.

In our example where we want to redirect our video web page from:

https://www.openbeelden.nl/media/1000452

to our new PeerTube web page:

https://peertube.beeldengeluid.nl/videos/watch/b0fd82cf-68b7-447d-a5fe-ed5706cd991a

you could map this with:

```
map $uri $new_uri {
    /media/1000452 /videos/watch/b0fd82cf-68b7-447d-a5fe-ed5706cd991a;
}
```

However this becomes a bit unwieldy when you have thousands of redirect like this. A clean way is to define all the redirects in a separate 'snippet' file `/etc/nginx/snippets/rewritemap.conf` and include this as follows:

```
map $uri $new_uri {
  include /etc/nginx/snippets/rewritemap.conf;
}
```

As we map redirects that always start with `/media` + old_id to one that starts with `/videos/watch` + new_id, further way to optimize this is to just map old_id to new_id and match the request with a seperate map block:

```
map $request_uri $old_id {
  ~^/media/([0-9]+) $1;
}

map $old_id $new_id {
  include /etc/nginx/snippets/rewritemap.conf;
}
```

with the included snippet that looks like:

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

and the redirect that is in the server block that checks if the variable `$new_id` has an assigned value:

```
server {
	
 if ($new_id) {
    return 301 /videos/watch/$new_id;
  }

}
```

Another reason for keeping the map directive’s key-value pairs (included via the snippet file) as small as possible is that Nginx uses [hash tables](https://nginx.org/en/docs/hash.html) to quickly process static sets of data.

When dealing with large sets of data (in our case thousands of id mappings) Nginx will throw this warning on start:

```
nginx: [warn] could not build optimal map_hash, you should increase either map_hash_max_size: 2048 or map_hash_bucket_size: 64; ignoring map_hash_bucket_size
```

As stated in the Nginx documentation:

> During the start and each re-configuration nginx selects the minimum possible sizes of hash tables such that the bucket size that stores keys with identical hash values does not exceed the configured parameter (hash bucket size). The size of a table is expressed in buckets. The adjustment is continued until the table size exceeds the hash max size parameter.

This means we have to set the `map_hash_max_size` and `map_hash_bucket_size` values before our mapping directive. The problem is that apart from the size of our data the processor also impacts what the optimal values are, which means we have to tweak these values and test them as it's practically impossible to estimate them beforehand.

The general recommendation would be to keep both values as small as possible.

* If nginx complains increase max_size first as long as it complains. If the number exceeds some big number (32769 for instance), increase bucket_size to multiple of default value on your platform as long as it complains. If it does not complain anymore, decrease max_size back as long as it does not complain. Now you have the best setup for your set of keys (each set of keys may need different setup).
* Bigger max_size means more memory consumed
* Bigger bucket_size means more CPU cycles (for every key lookup) and more transfers from main memory to cache.
* max_size is not related to number of keys directly, if number of keys doubles, you may need to increase max_size 10 times or even more to avoid collisions. If you cannot avoid them, you have to increase bucket_size.
* bucket_size is said to be increased to the next power of two, from the source code I would judge it should be enough to make it multiple of default value, this should keep transfers to cache optimal.
* Size of bucket_size depends on length of your keys. Should the average key size be 32 bytes (with hash array overhead), increasing bucket_size to 512 bytes would mean, that it can accommodate 16 keys with colliding hash key. This is not something that you want, if collision happens it searches linearly. You want to have as less collisions as possible.
* If you have max_size less than 10000 and small bucket_size, you can come across long loading time because nginx would try to find optimal hash size in a loop.
* If you have max_size bigger than 10000, there will be "only" 1000 loops performed before it would complain.

In our case with an id mapping set of 7200 items, we first increased the map_size and then tested our Ngnix reconfiguration with:

```sh
sudo nginx -t
```

We kept increasing it until there were no more Nginx warnings, but that resulted in a very big number, so then we doubled the bucket_size to 128 and then started again with the max_size by increasing it with a factor of 2 from the original 1024. This resulted in the following mapping directive after testing:

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

In our previous article on [bulk importing videos](https://beeldengeluid.github.io/extending-peertube/migration/2021/07/06/importing-videos-with-the-api.html) to a PeerTube instance with the API, you can find how and where we generated the snippet file `rewritemap.conf` with the old ids from our data in the CSV file and the new ids from the PeerTube API response on succesfull import/upload.

In our next article we will show how to integrate this Nginx URL redirection setup in PeerTube (or in any other existing webserver with Nginx), by recommending where to add these Nginx configuration files.
