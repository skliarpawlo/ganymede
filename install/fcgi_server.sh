#!/bin/bash

case "$1" in
"start")
        ../manage.py runfcgi method=prefork host=127.0.0.1 port=8881 pidfile=/var/run/pyfcgi.pid
;;
"stop")
        kill -9 `cat /var/run/pyfcgi.pid`
;;
"restart")
        $0 stop
        sleep 1
        $0 start
;;
*)
        echo "Usage: ./fcgi_server.sh {start|stop|restart}"
;;
esac