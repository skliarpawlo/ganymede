PID_FILE=/home/skliar/ganymede.lun.ua/logs/ganymede.pid
SOCKET=/home/skliar/ganymede.lun.ua/logs/ganymede.sock
ERR_LOG=/home/skliar/ganymede.lun.ua/logs/fcgi.err
DEBUG_SERVER=0.0.0.0
DEBUG_PORT=8181

../../manage.py runserver $DEBUG_SERVER:$DEBUG_PORT