server
{
	listen 80;
	server_name ganymede.lun.ua;

	charset utf-8;
	access_log /home/pavlo/logs/ganymede.access.log;
	error_log /home/pavlo/logs/ganymede.error.log;

	location /
	{
		fastcgi_pass unix:/home/pavlo/logs/ganymede.sock;
		include py_fastcgi_params;
	}

	location /static/
	{
		root /home/pavlo/main/ganymede;
	}
}
