server
{
	listen 80;
	server_name ganymede.lun.ua;

	charset utf-8;
	access_log /home/skliar/ganymede.lun.ua/logs/ganymede.access.log;
	error_log /home/skliar/ganymede.lun.ua/logs/ganymede.error.log;

	location /
	{
		fastcgi_pass unix:/home/skliar/ganymede.lun.ua/logs/ganymede.sock;
		include py_fastcgi_params;
	}

	location /static/
	{
		root /home/skliar/ganymede.lun.ua/main/ganymede;
	}
}
