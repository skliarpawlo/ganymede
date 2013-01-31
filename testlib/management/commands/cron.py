from django.core.management.base import BaseCommand
from testlib import tasks
from core import db

class Command(BaseCommand):
    def handle(self, *args, **options):
        db.init()
        tasks.run_all()
        db.close()
