#!/bin/bash

PID_FILE=/home/pavlo/logs/ganymede.pid
SOCKET=/home/pavlo/logs/ganymede.sock
ERR_LOG=/home/pavlo/logs/fcgi.err

case "$1" in
"start")
        sudo -u www-data ../manage.py runfcgi method=prefork socket=$SOCKET pidfile=$PID_FILE errlog=$ERR_LOG
;;
"stop")
        kill -9 `cat $PID_FILE`
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
