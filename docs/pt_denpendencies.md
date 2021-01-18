ffmpeg -version # Should be >= 4.1
g++ -v # Should be >= 5.x
redis-server -v # Should be >= 2.8.18
nodejs -v # Should be >= 10.x
yarn -v # Should be >= 1.x
postgres -V # Should be >= 9.6

If the postgres binary is not in system's PATH, you'll get an error saying "postgres: command not found". This usually happens when the PostgreSQL package is not installed from the distribution's standard repositories.

You can find the path to the binary either with the `locate` or `find` command:

```sh
sudo find /usr -wholename '*/bin/postgres'
```

or

```sh
sudo updatedb
locate bin/postgres
```

The output should look something like this:

```
/usr/lib/postgresql/9.6/bin/postgres
```

Once you find the path to the binary, you can use it to get the version of the PostgreSQL server:

```
/usr/lib/postgresql/9.6/bin/postgres -V
```

sudo updatedb
locate bin/postgres


Dependencies
nginx
PostgreSQL >= 9.6
Redis >= 2.8.18
NodeJS >= 10.x
yarn >= 1.x
FFmpeg >= 4.1