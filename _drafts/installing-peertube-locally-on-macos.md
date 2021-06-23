---
layout: post
title: Installing PeerTube on macOS
category: Tools
comments: false
---

Part of the setup for [developing a PeerTube plugin](https://beeldengeluid.github.io/extending-peertube/cc%20plugin/2021/06/16/developing-a-peertube-plugin), is to install a PeerTube instance locally. The [contributing](https://github.com/Chocobozzz/PeerTube/blob/develop/.github/CONTRIBUTING.md#develop) and [dependencies](https://github.com/Chocobozzz/PeerTube/blob/develop/support/doc/dependencies.md) docs explain how to clone the PeerTube repository, install dependencies and prepare the database. These resources also offer some OS specific tips. In this article we expand on some issues we ran into during installation on macOS, which is one of the operating systems we used for development.

> ... the other ones being Ubuntu in VMware, Ubuntu on WSL2, Ubuntu and [Fedora](https://github.com/beeldengeluid/extending-peertube/issues/1) on bare metal

<!--more-->

While following the [dependencies guide for installation on macOS](https://github.com/Chocobozzz/PeerTube/blob/develop/support/doc/dependencies.md#macos), we ran into a `unknown user: postgres` error. We have made a suggestion to describe this error more clearly in the guide, which has since [been updated](https://github.com/Chocobozzz/PeerTube/pull/4051).

The provided solution of using `_postgres` instead of `postgres` as user name, resolved the error. However, using the `_postgres` user also brought along a permission issue:

```sh
$ sudo -u _postgres createuser -U peertube
Password:
could not identify current directory: Permission denied
createuser: error: could not connect to database template1: FATAL:  role "peertube" does not exist
```

As our current set up is for local development only, we ended up bypassing this by running as our current user, which has the right permissions:

```sh
createuser -P peertube
createdb -O peertube peertube_dev
```

Lastly, while testing that postgress was working properly, the `psql` command line tool expected a database with the name equal to the current user:

```sh
$ psql
psql: error: FATAL:  database "myawesomeusername" does not exist
```

We fixed this by creating that database:

```sh
createdb myawesomeusername
```

With a local database set up, the remaining [prerequisites](https://github.com/Chocobozzz/PeerTube/blob/develop/.github/CONTRIBUTING.md#prerequisites) can be followed. 

Once all prerequisites are met, we are ready to spin up our local PeerTube instance' client and server side:

```sh
npm run dev
```

We can keep this command running while we are [developing our plugin](https://beeldengeluid.github.io/extending-peertube/cc%20plugin/2021/06/16/developing-a-peertube-plugin), to see the updated functionality reflected in our browser.
