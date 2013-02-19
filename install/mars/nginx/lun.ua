server {
    listen 80;
    server_name lun.ua;
    rewrite ^ $scheme://www.lun.ua$request_uri? permanent;
}
server {
    listen 80;
    server_name ~^www\.(?<subdomain>(conference|novostroyki|cottage|cherkassy|chernigov|chernovtsy|dnepropetrovsk|donetsk|gorlovka|ivano-frankovsk|kharkov|kherson|khmelnitsky|kirovograd|kremenchug|lugansk|lutsk|lvov|makeevka|mariupol|nikolaev|odessa|poltava|rovno|sevastopol|simferopol|sumy|ternopol|uzhgorod|vinnica|yalta|zaporozhe|zhitomir)).lun.ua$;
    rewrite ^ $scheme://$subdomain.lun.ua$request_uri? permanent;
}
server {
    listen 80;
    server_name www.lun.ua ~^(?<subdomain>(conference|novostroyki|cottage|cherkassy|chernigov|chernovtsy|dnepropetrovsk|donetsk|gorlovka|ivano-frankovsk|kharkov|kherson|khmelnitsky|kirovograd|kremenchug|lugansk|lutsk|lvov|makeevka|mariupol|nikolaev|odessa|poltava|rovno|sevastopol|simferopol|sumy|ternopol|uzhgorod|vinnica|yalta|zaporozhe|zhitomir)).lun.ua$;

    access_log /home/skliar/ganymede.lun.ua/logs/www.lun.ua.access.log;
    error_log /home/skliar/ganymede.lun.ua/logs/www.lun.ua.error.log;

    charset utf-8;

    root /home/skliar/ganymede.lun.ua/lun.ua;
    index index.php index.html index.htm;

    location ~ ^.+/$ {
	rewrite ^(.+)/$ $1 permanent;
    }

    location / {
#	rewrite ^.*$ http://www.lun.ua/sorry redirect;
	try_files $uri @yii;
    }

    # temporary rewrites

    location = /bigmir/realty/city=1&contractType=6&realtyType=1 {
	rewrite /bigmir/realty/city=1&contractType=6&realtyType=1 http://www.lun.ua/bigmir/realty/search?city=1&contractType=6&realtyType=1&url=http://finance.bigmir.net/realty/lun permanent;
    }

    location = /home/partners {
	rewrite /home/partners http://www.lun.ua/partners permanent;
    }

    location = /www {
	rewrite /www http://www.lun.ua/ permanent;
    }

    location = /realty/search/rent/flat.html {
	rewrite /realty/search/rent/flat.html http://www.lun.ua/аренда-квартир-киев permanent;
    }

    # end temporary rewrites

    location ~ ^/redirect/\d+.*$ {
	rewrite ^(.*)/redirect/(\d+)(.*)$ $1/a/$2/redirect$3 permanent;
    }

    location /css {
	access_log off;
    }

    location /images {
	access_log off;
    }

    location /js {
	access_log off;
    }

    location /assets {
	access_log off;
    }

    location = /sorry {
	access_log off;
	try_files $uri @yii;
    }

    location = /i/counter.png {
	access_log off;
	try_files $uri /images/counter.png;
    }

    location = /favicon.ico {
	log_not_found off;
	access_log off;
    }

    location = /robots.txt {
	log_not_found off;
	access_log off;
    }

    location ~* -s0-\d+$ {
	log_not_found off;
	access_log off;
	return 404;
    }

    location ~* -s0-\d+\|\d+$ {
	log_not_found off;
	access_log off;
	return 404;
    }

    location ~* -s0-\d+..?$ {
	log_not_found off;
	access_log off;
	return 404;
    }

    location ~* -s0$ {
	log_not_found off;
	access_log off;
	return 404;
    }

    location ~ \.php$ {
	return 404;
    }

    location /api1/ {
        gzip on;
        gzip_buffers 64 8k;
        gzip_comp_level 9;
        gzip_disable "msie6";
        gzip_min_length 0;
        gzip_http_version 1.0;
        gzip_proxied any;
        gzip_types *;
        gzip_vary on;
        try_files $uri @yii;
    }

    location @yii {
	fastcgi_pass 127.0.0.1:9000;
	fastcgi_param SCRIPT_FILENAME $document_root/index.php;
	fastcgi_param PATH_INFO $fastcgi_script_name;
	fastcgi_param QUERY_STRING $uri;
	include fastcgi_params;
	fastcgi_connect_timeout 300;
	fastcgi_send_timeout 600;
	fastcgi_read_timeout 600;
    }

    # deny access to .htaccess files, if Apache's document root concurs with nginx's one
    location ~ /\.ht {
	deny  all;
    }
}