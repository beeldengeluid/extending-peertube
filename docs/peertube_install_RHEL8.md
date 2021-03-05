PeerTube installation on Redhat 8
---------------------------------

- Node.js
- Yarn
- FFmpeg

```
sudo dnf module install nodejs:12
sudo curl --silent --location https://dl.yarnpkg.com/rpm/yarn.repo | sudo tee /etc/yum.repos.d/yarn.repo
sudo dnf install yarn

sudo dnf install epel-release
sudo dnf install --nogpgcheck https://mirrors.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm 

sudo dnf install ffmpeg ffmpeg-devel

```

- nginx
- Postgres
- Redis
- oident
- (misc)

```
sudo dnf install nginx postgresql postgresql-server postgresql-contrib oidentd openssl gcc-c++ make wget redis git

sudo postgresql-setup initdb
sudo systemctl enable postgresql.service
sudo systemctl start postgresql.service

sudo systemctl enable nginx.service
sudo systemctl start nginx.service

sudo systemctl enable redis.service
sudo systemctl start redis.service

sudo systemctl enable oident.service
sudo systemctl start oident.service

sudo ln -s /usr/bin/python3 /usr/bin/python

```

### peertube user

```
sudo mkdir /var/www 
sudo chmod 755 www
sudo useradd -m -d /var/www/peertube -s /bin/bash -p peertube peertube
sudo passwd peertube
sudo chmod 755 peertube

```

Note:

- Missing /var/www folder? Check if RHEL doesn't add this in default setup

### Database

```
sudo -u postgres createuser -P peertube
sudo -u postgres createdb -O peertube -E UTF8 -T template0 peertube_prod

sudo -u postgres psql -c "CREATE EXTENSION pg_trgm;" peertube_prod
sudo -u postgres psql -c "CREATE EXTENSION unaccent;" peertube_prod

```

### PeerTube

```
sudo -i

VERSION=$(curl -s https://api.github.com/repos/chocobozzz/peertube/releases/latest | grep tag_name | cut -d '"' -f 4) && echo "Latest Peertube version is $VERSION"

cd /var/www/peertube
sudo -u peertube mkdir config storage versions
cd /var/www/peertube/versions
sudo -u peertube wget -q "https://github.com/Chocobozzz/PeerTube/releases/download/${VERSION}/peertube-${VERSION}.zip"
sudo -u peertube unzip peertube-${VERSION}.zip && sudo -u peertube rm peertube-${VERSION}.zip

cd /var/www/peertube
sudo -u peertube ln -s versions/peertube-${VERSION} ./peertube-latest
cd ./peertube-latest && sudo -H -u peertube yarn install --production --pure-lockfile

```

### PeerTube configuration

```
cd /var/www/peertube
sudo -u peertube cp peertube-latest/config/default.yaml config/default.yaml

cd /var/www/peertube
sudo -u peertube cp peertube-latest/config/production.yaml.example config/production.yaml

vim config/production.yaml

```

Then edit the config/production.yaml file according to your webserver and database configuration (webserver, database, redis, smtp and admin.email sections in particular). Keys defined in config/production.yaml will override keys defined in config/default.yaml.

NOTE:

- smtp.beeldengeluid.nl on port 25
- from_address and admin.email on fstrater@beeldengeluid.nl (or other @beeldengeluid.nl)

### Storage

```
cd /mnt/peertube
mkdir sudo -u peertube storage
chmod -R 755 storage

mount --bind /mnt/peertube/storage /var/www/peertube/storage

```

NOTE:

- Store the mount in /etc/fstab (so it is recovered after reboot); add the following to the bottom of the file:
	

/mnt/peertube/storage /var/www/peertube/storage none defaults,bind,umask=000,dmask=027,fmask=137,uid=peertube,gid=root 0 0


### Webserver

```
mkdir /etc/nginx/sites-available
mkdir /etc/nginx/sites-enabled
sudo cp /var/www/peertube/peertube-latest/support/nginx/peertube /etc/nginx/sites-available/peertube
sudo ln -s /etc/nginx/sites-available/peertube /etc/nginx/sites-enabled/peertube
sudo ln -s /etc/nginx/sites-enabled/peertube /etc/nginx/conf.d/peertube.conf

sudo sed -i 's/${WEBSERVER_HOST}/peertube.beeldengeluid.nl/g' /etc/nginx/sites-available/peertube
sudo sed -i 's/${PEERTUBE_HOST}/127.0.0.1:9000/g' /etc/nginx/sites-available/peertube

sudo systemctl stop nginx

```

NOTE:

- disable 'aio=threads' in /etc/nginx/conf.d/peertube.conf, because no multithreading on this server?
- create fullchain certificate (fullchain.pem) from WILDCARD_beeldengeluid_nl.crt and Sectigo_PositiveSSL_bundle.crt
- add fullchain.pem in /etc/pki/tls/certs/ and star_beeldengeluid_nl.key /etc/pki/tls/private/
- add key and pem in /etc/nginx/conf.d/peertube.conf

```
sudo systemctl start nginx

```

### TCP/IP Tuning

```
sudo cp /var/www/peertube/peertube-latest/support/sysctl.d/30-peertube-tcp.conf /etc/sysctl.d/
sudo sysctl -p /etc/sysctl.d/30-peertube-tcp.conf

sudo cp /var/www/peertube/peertube-latest/support/systemd/peertube.service /etc/systemd/system/
sudo systemctl daemon-reload

sudo systemctl enable peertube

```

### Run

```
sudo systemctl start peertube
sudo journalctl -feu peertube

```

