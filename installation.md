# Installation on Ubuntu 18.04 LTS

### PeerTube user

Create a `peertube` user with `/var/www/peertube` home:

```bash
$ sudo useradd --create-home --home-dir /var/www/peertube --shell /bin/bash --password peertube peertube
```

