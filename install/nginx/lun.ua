server {
    server_name posutochno.lun.ua www.posutochno.lun.ua;
    return 302 http://www.lun.ua/посуточная-аренда-квартир-киев;
}
server {
    server_name lun.ua;
    return 301 $scheme://www.lun.ua$request_uri;
}
server {
    server_name ~^www\.(?<subdomain>(conference|novostroyki|cottage|office|cherkassy|chernigov|chernovtsy|dnepropetrovsk|donetsk|gorlovka|ivano-frankovsk|kharkov|kherson|khmelnitsky|kirovograd|kremenchug|lugansk|lutsk|lvov|makeevka|mariupol|nikolaev|odessa|poltava|rovno|sevastopol|simferopol|sumy|ternopol|uzhgorod|vinnica|yalta|zaporozhe|zhitomir)).lun.ua$;
    return 301 $scheme://$subdomain.lun.ua$request_uri;
}
server {
    listen 80 default_server;
    server_name www.lun.ua ~^(?<subdomain>(conference|novostroyki|cottage|office|cherkassy|chernigov|chernovtsy|dnepropetrovsk|donetsk|gorlovka|ivano-frankovsk|kharkov|kherson|khmelnitsky|kirovograd|kremenchug|lugansk|lutsk|lvov|makeevka|mariupol|nikolaev|odessa|poltava|rovno|sevastopol|simferopol|sumy|ternopol|uzhgorod|vinnica|yalta|zaporozhe|zhitomir)).lun.ua$;

    root /home/pavlo/main/test;

    access_log /home/pavlo/logs/www.lun.ua.access.log;
    error_log /home/pavlo/logs/www.lun.ua.error.log;

    charset utf-8;

    deny 91.222.137.17;
    deny 91.202.128.29;
    deny 49.0.124.86;
    deny 89.218.0.186;
    deny 2.133.93.242;
    deny 203.198.23.82;
    deny 190.52.120.38;
    deny 210.242.4.253;
    deny 178.151.216.90;
    deny 61.91.89.29;
    deny 91.231.40.53;
    deny 91.231.40.54;
    deny 77.94.48.4;
    deny 201.218.130.46;
    deny 85.118.227.75;
    deny 147.31.182.137;
    deny 113.254.11.28;

    location ~ ^.+/$ {
	rewrite ^(.+)/$ $1 permanent;
    }

    if ($http_x_forwarded_for = '91.222.137.17') {
	    return 403;
    }

    location / {
#	rewrite ^.*$ http://www.lun.ua/sorry redirect;
	try_files $uri @yii;
    }

    # temporary rewrites

    location = /аренда-квартир-барышевка-2-1-5380 {
	rewrite /аренда-квартир-барышевка-2-1-5380 http://www.lun.ua/аренда-квартир-барышевка permanent;
    }

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
	include fastcgi_params;
	fastcgi_param SCRIPT_FILENAME $document_root/index.php;
	fastcgi_param PATH_INFO $fastcgi_script_name;
	fastcgi_connect_timeout 300;
	fastcgi_send_timeout 600;
	fastcgi_read_timeout 600;
#	fastcgi_pass fpm.lun.ua;
#	fastcgi_pass 127.0.0.1:9009;
	fastcgi_pass 127.0.0.1:9000;
#	fastcgi_pass unix:/var/run/lun.ua-fpm.sock;
#	fastcgi_pass 77.120.117.29:9010;
    }

    # deny access to .htaccess files, if Apache's document root concurs with nginx's one
    location ~ /\.ht {
	deny all;
    }

    location /static {
	deny all;
    }

    location /protected {
	deny all;
    }

    location /scripts {
	deny all;
    }

    location = /stat {
	stub_status on;
	access_log off;
	allow 80.64.95.177;
	deny all;
    }
}