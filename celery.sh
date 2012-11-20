#!/usr/bin/env bash
#starting celery worker (jobs executer)
./manage.py celery worker --quiet --logfile=/var/log/celery/worker.log &
#starting celery beat (timer)
./manage.py celery beat --quiet --logfile=/var/log/celery/beat.log &
