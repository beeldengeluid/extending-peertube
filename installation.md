# PeerTube installation on localhost

This installation guide is written for installing PeerTube on localhost for testing and demo purposes. Although this guide uses Ubuntu 18.04 LTS desktop as target OS for the server and client, it can be used for other Linux distributions as well. Further information on differences in installation steps can be found in the official PeerTube [Production Guide](https://github.com/Chocobozzz/PeerTube/blob/develop/support/doc/production.md)

## Requirements

For installation on localhost you either need a Virtual Machine or a desktop/laptop with a fresh (and updated) install of a Linux desktop distribution with the following requirements:

* RAM: 1GB or more
* CPU: 1 core if you don't enable transcoding, 2 at least if you enable it (works with 1 but this is really slow)
* Storage: completely depends on how many videos you will upload

## Dependencies

As root user, install basic utility programs needed for the installation:

(On Ubuntu `sudo` is already pre-installend, so you can use `sudo -s` to get to root)

```bash
# apt-get install curl sudo unzip vim
```

It would be wise to disable root access and to continue this tutorial with a user with sudoers group access.

Next you have to install the following dependencies:

* nginx
* PostgreSQL >= 9.6
* Redis >= 2.8.18
* NodeJS >= 8.x
* yarn >= 1.x
* FFmpeg >= 3.x

First start with NodeJS (and npm) and Yarn:

```bash
$ sudo apt install nodejs npm -y
```

For Yarn we need an extra source in the repositories list otherwise Ubuntu recommends you to install the `cmdtest` package (which contains a binary with the same name `yarn`).

```bash
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt update
sudo apt install yarn
```

Then continue with the rest:

```bash
$ sudo apt install nginx ffmpeg postgresql postgresql-contrib openssl g++ make redis-server git python-dev
```

Now that dependencies are installed, before running PeerTube you should start PostgreSQL and Redis:

```bash
$ sudo systemctl start redis postgresql
```

## Localhost

Before starting the installation you have to decide on a domain name which you will use as an alias for localhost. The chosen domain name cannot be altered after you start using your PeerTube instance. Something like https://peertube.yourcompany.com will be fine.

Your chosen domain name then needs to be added to your local DNS. For this you add an entry as follows:

```bash
$ sudo vim /etc/hosts
```

Just add `127.0.0.1 peertube.yourcompany.com` to the existing list of localhost aliases.

## HTTPS

HTTPS is needed for the client connection to the PeerTube instance, so a valid certificate needs to be generated for localhost. For this you can use `mkcert` as a simple solution.

https://blog.filippo.io/mkcert-valid-https-certificates-for-localhost/

First install `certutil`:

```bash
$ sudo apt install libnss3-tools
```

Then download the binary to /usr/local/bin/ and make it executable:

```bash
sudo wget https://github.com/FiloSottile/mkcert/releases/download/v1.3.0/mkcert-v1.3.0-linux-amd64 -O /usr/local/bin/mkcert
sudo chmod +x /usr/local/bin/mkcert
```

Now you can use it by generating a local Certificate Authority (CA):

```bash
$ mkcert -install
```

And generate certificate for the localhost domain name:

```bash
$ mkcert peertube.yourcompany.com localhost 127.0.0.1 ::1
```

The two `.pem` files will be moved later into the PeerTube installation. 

## PeerTube installation

The following steps for installation of PeerTube (user, database, directories, installation) are the same as in the official PeerTube [Production Guide](https://github.com/Chocobozzz/PeerTube/blob/develop/support/doc/production.md)


### PeerTube user

Create a `peertube` user with `/var/www/peertube` home:

```bash
$ sudo useradd -m -d /var/www/peertube -s /bin/bash -p peertube peertube
```

Set its password:

```bash
$ sudo passwd peertube
```

### Database

Create the production database and a peertube user inside PostgreSQL:

```bash
$ sudo -u postgres createuser -P peertube
$ sudo -u postgres createdb -O peertube peertube_prod
```

Then enable extensions PeerTube needs:

```bash
$ sudo -u postgres psql -c "CREATE EXTENSION pg_trgm;" peertube_prod
$ sudo -u postgres psql -c "CREATE EXTENSION unaccent;" peertube_prod
```

### Prepare PeerTube directory

Fetch the latest tagged version of Peertube

```bash
$ VERSION=$(curl -s https://api.github.com/repos/chocobozzz/peertube/releases/latest | grep tag_name | cut -d '"' -f 4) && echo "Latest Peertube version is $VERSION"
```

Open the peertube directory, create a few required directories

```bash
$ cd /var/www/peertube && sudo -u peertube mkdir config storage versions && cd versions
```

Download the latest version of the Peertube client, unzip it and remove the zip

```bash
$ sudo -u peertube wget -q "https://github.com/Chocobozzz/PeerTube/releases/download/${VERSION}/peertube-${VERSION}.zip"
$ sudo -u peertube unzip peertube-${VERSION}.zip && sudo -u peertube rm peertube-${VERSION}.zip
```

Install Peertube:

```bash
$ cd ../ && sudo -u peertube ln -s versions/peertube-${VERSION} ./peertube-latest
$ cd ./peertube-latest && sudo -H -u peertube yarn install --production --pure-lockfile
```

## PeerTube configuration

Copy example configuration:

```bash
$ cd /var/www/peertube && sudo -u peertube cp peertube-latest/config/production.yaml.example config/production.yaml
```

Then edit the `config/production.yaml` file according to your webserver configuration. At least you should change hostname under webserver to peertube.yourcompany.com and the password under database to the password you chose when creating the PostgreSQL peertube user.

## Webserver

Copy the nginx configuration template:

```bash
$ sudo cp /var/www/peertube/peertube-latest/support/nginx/peertube /etc/nginx/sites-available/peertube
```

Then modify the webserver configuration file. Please pay attention to the `alias` keys of the static locations.
It should correspond to the paths of your storage directories (set in the configuration file inside the `storage` key).

```bash
$ sudo vim /etc/nginx/sites-available/peertube
```

Change the domain name globally by using this command in vim:

```
:%s/peertube.example.com/peertube.yourcompany.com/g
```

Update the paths to the SSL certificates to `/var/www/peertube.yourcompany.com+3.pem` and `/var/www/peertube.yourcompany.com+3-key.pem` and move the two `.pem` files with (assuming you generated them in your home directory with mkcert):

```bash
$ sudo mv ~/peertube.yourcompany.com+3.pem /var/www/peertube.yourcompany.com+3.pem
$ sudo mv ~/peertube.yourcompany.com+3-key.pem /var/www/peertube.yourcompany.com+3-key.pem
```

Activate the configuration file:

```bash
$ sudo ln -s /etc/nginx/sites-available/peertube /etc/nginx/sites-enabled/peertube
```

Now you have the certificates you can reload nginx:

```bash
$ sudo systemctl reload nginx
```

## TCP/IP Tuning

```bash
$ sudo cp /var/www/peertube/peertube-latest/support/sysctl.d/30-peertube-tcp.conf /etc/sysctl.d/
$ sudo sysctl -p /etc/sysctl.d/30-peertube-tcp.conf
```

Your distro may enable this by default, but at least Debian 9 does not, and the default FIFO
scheduler is quite prone to "Buffer Bloat" and extreme latency when dealing with slower client
links as we often encounter in a video server.

### systemd

If your OS uses systemd, copy the configuration template:

```bash
$ sudo cp /var/www/peertube/peertube-latest/support/systemd/peertube.service /etc/systemd/system/
```

Update the service file:

```bash
$ sudo vim /etc/systemd/system/peertube.service
```

Tell systemd to reload its config:

```bash
$ sudo systemctl daemon-reload
```

If you want to start PeerTube on boot:

```bash
$ sudo systemctl enable peertube
```

Run:

```bash
$ sudo systemctl start peertube
$ sudo journalctl -feu peertube
```

## Administrator

The administrator (root) password is automatically generated and can be found in the logs. You can set another password with:

```bash
$ cd /var/www/peertube/peertube-latest && NODE_CONFIG_DIR=/var/www/peertube/config NODE_ENV=production npm run reset-password -- -u root
```