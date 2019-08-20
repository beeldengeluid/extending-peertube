# PeerTube configuration

Although the configuration was touched upon during the installation, this article will explain all the configurable options in the file `/var/www/peertube/config/production.yaml` which can't be changed through the Administration interface when logged in as root/admin.

```yaml
listen:
  hostname: 'localhost'
  port: 9000
```

Normally there is no need to change this. TCP port 9000 is where the PeerTube server application runs on.  

```yaml
# Correspond to your reverse proxy server_name/listen configuration
webserver:
  https: true
  hostname: 'example.com'
  port: 443
```

The hostname needs to be changed (to something like 'peertube.yourcompany.com') and it should match server_name in your Nginx configuration in `/etc/nginx/sites-available/peertube`

```yaml
rates_limit:
  api:
    # 50 attempts in 10 seconds
    window: 10 seconds
    max: 50
  login:
    # 15 attempts in 5 min
    window: 5 minutes
    max: 15
  signup:
    # 2 attempts in 5 min (only succeeded attempts are taken into account)
    window: 5 minutes
    max: 2
  ask_send_email:
    # 3 attempts in 5 min
    window: 5 minutes
    max: 3
```

These settings are important to prevent automated spam and DOS attacks. You might want to change the rates limit for the API when you are using the API for your own bulk migration.

```yaml
# Proxies to trust to get real client IP
# If you run PeerTube just behind a local proxy (nginx), keep 'loopback'
# If you run PeerTube behind a remote proxy, add the proxy IP address (or subnet)
trust_proxy:
  - 'loopback'
```

Normally there is no need to change this.


```yaml
# Your database name will be "peertube"+database.suffix
database:
  hostname: 'localhost'
  port: 5432
  suffix: '_prod'
  username: 'peertube'
  password: 'peertube'
  pool:
    max: 5
```

You need to update the password to that which you have chosen during installation.

```yaml
# Redis server for short time storage
# You can also specify a 'socket' path to a unix socket but first need to
# comment out hostname and port
redis:
  hostname: 'localhost'
  port: 6379
  auth: null
  db: 0
```

Normally there is no need to change this.

```yaml
# SMTP server to send emails
smtp:
  hostname: null
  port: 465 # If you use StartTLS: 587
  username: null
  password: null
  tls: true # If you use StartTLS: false
  disable_starttls: false
  ca_file: null # Used for self signed certificates
  from_address: 'admin@example.com'
```

To be able to send email from PeerTube there needs to be an available SMTP server. A setup with [postfix](http://www.postfix.org/) is recommended, but for testing purposes you could use a Gmail account and the free Gmail SMTP server `smtp.gmail.com`. See for instructions: https://support.google.com/a/answer/176600?hl=en

```yaml
email:
  body:
    signature: "PeerTube"
  object:
    prefix: "[PeerTube]"
```

Change this accordingly to how you want to prefix the subject line and to sign the automated emails messages from your instance.

```yaml
# From the project root directory
storage:
  tmp: '/var/www/peertube/storage/tmp/' # Used to download data (imports etc), store uploaded files before processing...
  avatars: '/var/www/peertube/storage/avatars/'
  videos: '/var/www/peertube/storage/videos/'
  streaming_playlists: '/var/www/peertube/storage/streaming-playlists/'
  redundancy: '/var/www/peertube/storage/videos/'
  logs: '/var/www/peertube/storage/logs/'
  previews: '/var/www/peertube/storage/previews/'
  thumbnails: '/var/www/peertube/storage/thumbnails/'
  torrents: '/var/www/peertube/storage/torrents/'
  captions: '/var/www/peertube/storage/captions/'
  cache: '/var/www/peertube/storage/cache/'
  plugins: '/var/www/peertube/storage/plugins/'
```

Normally there is no need to change this.

```yaml
log:
  level: 'info' # debug/info/warning/error
  rotation:
    enabled : true
```

Normally there is no need to change this.

```yaml
search:
  # Add ability to fetch remote videos/actors by their URI, that may not be federated with your instance
  # If enabled, the associated group will be able to "escape" from the instance follows
  # That means they will be able to follow channels, watch videos, list videos of non followed instances
  remote_uri:
    users: true
    anonymous: false
```

Normally there is no need to change this.

```yaml
trending:
  videos:
    interval_days: 7 # Compute trending videos for the last x days
```

Normally there is no need to change this.

```yaml
# Cache remote videos on your server, to help other instances to broadcast the video
# You can define multiple caches using different sizes/strategies
# Once you have defined your strategies, choose which instances you want to cache in admin -> manage follows -> following
redundancy:
  videos:
    check_interval: '1 hour' # How often you want to check new videos to cache
    strategies: # Just uncomment strategies you want
#      -
#        size: '10GB'
#        # Minimum time the video must remain in the cache. Only accept values > 10 hours (to not overload remote instances)
#        min_lifetime: '48 hours'
#        strategy: 'most-views' # Cache videos that have the most views
#      -
#        size: '10GB'
#        # Minimum time the video must remain in the cache. Only accept values > 10 hours (to not overload remote instances)
#        min_lifetime: '48 hours'
#        strategy: 'trending' # Cache trending videos
#      -
#        size: '10GB'
#        # Minimum time the video must remain in the cache. Only accept values > 10 hours (to not overload remote instances)
#        min_lifetime: '48 hours'
#        strategy: 'recently-added' # Cache recently added videos
#        min_views: 10 # Having at least x views
```

Normally there is no need to change this.

```yaml
csp:
  enabled: false
  report_only: true # CSP directives are still being tested, so disable the report only mode at your own risk!
  report_uri:
```

Normally there is no need to change this.

```yaml
tracker:
  # If you disable the tracker, you disable the P2P aspect of PeerTube
  enabled: true
  # Only handle requests on your videos.
  # If you set this to false it means you have a public tracker.
  # Then, it is possible that clients overload your instance with external torrents
  private: true
  # Reject peers that do a lot of announces (could improve privacy of TCP/UDP peers)
  reject_too_many_announces: false
```

Normally there is no need to change this, unless you want to disabe the P2P streaming.

```yaml
history:
  videos:
    # If you want to limit users videos history
    # -1 means there is no limitations
    # Other values could be '6 months' or '30 days' etc (PeerTube will periodically delete old entries from database)
    max_age: -1
```

Normally there is no need to change this.

```yaml
views:
  videos:
    # PeerTube creates a database entry every hour for each video to track views over a period of time
    # This is used in particular by the Trending page
    # PeerTube could remove old remote video views if you want to reduce your database size (video view counter will not be altered)
    # -1 means no cleanup
    # Other values could be '6 months' or '30 days' etc (PeerTube will periodically delete old entries from database)
    remote:
      max_age: -1
```

Normally there is no need to change this.

```yaml
plugins:
  # The website PeerTube will ask for available PeerTube plugins
  # This is an unmoderated plugin index, so only install plugins you trust
  index:
    enabled: true
    check_latest_versions_interval: '12 hours' # How often you want to check new plugins/themes versions
    url: 'https://packages.joinpeertube.org'
```

This setting is for the upcoming plugin functionality in version 1.4

As the following comment shows, the other configuration options can be changed through the administration interface. 

```yaml
###############################################################################
#
# From this point, all the following keys can be overridden by the web interface
# (local-production.json file). If you need to change some values, prefer to
# use the web interface because the configuration will be automatically
# reloaded without any need to restart PeerTube.
#
# /!\ If you already have a local-production.json file, the modification of the
# following keys will have no effect /!\.
#
###############################################################################
```

There's one exception and that is setting the admin email before first startup.

```yaml
admin:
  # Used to generate the root user at first startup
  # And to receive emails from the contact form
  email: 'admin@example.com'
```