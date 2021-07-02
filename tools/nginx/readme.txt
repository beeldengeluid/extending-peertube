/etc/nginx/conf.d/redirect.conf
--------------------------------

map $request_uri $old_id {
	/media/([0-9]+) $1;
}

map $old_id $new_id {
	include /etc/nginx/snippets/rewritemap.map;
}

/etc/nginx/conf.d/peertube.conf
--------------------------------

server {
	if ($new_id) {
    return 301 /videos/watch/$new_id;
  }
}

/etc/nginx/snippets/rewritemap.map
----------------------------------
1239795 c29558d2-bf21-4f19-a90a-085caaf83f43;




Notes:

peertube.conf is a symlink to /etc/nginx/sites-enabled/peertube
(sudo ln -s /etc/nginx/sites-enabled/peertube /etc/nginx/conf.d/peertube.conf)

vim add semicolon to each line:

:%s/$/;