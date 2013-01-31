PID_FILE=/home/pavlo/logs/ganymede.pid
SOCKET=/home/pavlo/logs/ganymede.sock
ERR_LOG=/home/pavlo/logs/fcgi.err
DEBUG_SERVER=0.0.0.0
DEBUG_PORT=8181

../manage.py runserver $DEBUG_SERVER:$DEBUG_PORT