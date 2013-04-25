from django.core.management.base import BaseCommand
from testing_runtime.models import Task, Job
from core import db
from threading import Timer

def add_task( job_id ) :
    db.reconnect()
    new_task = Task( job_id = job_id, status='waiting', whose='cron [daily]' )
    db.session.add( new_task )
    db.session.commit()

def delayed_exec(time, func, args):
    delay = time.hour * 60 * 60 + time.minute * 60
    if delay >= 0:
        Timer(delay, func, args).start()


class Command(BaseCommand):
    def handle(self, *args, **options):
        db.init()
        jobs_to_exec = db.session.query( Job ).filter( Job.exec_time != None ).all()
        jobs_ids = []
        for job in jobs_to_exec :
            jobs_ids.append( (job.job_id, job.exec_time) )
        db.close()

        for job_id, exec_time in jobs_ids :
            delayed_exec(
                exec_time,
                add_task,
                ( job_id, )
            )

