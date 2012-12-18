from django.core.management.base import BaseCommand
from tests import tasks
from core import db
from core import mode

class Command(BaseCommand):
    def handle(self, *args, **options):
        db.init()
        mode.set( mode.PRODUCTION )

        tasks.run_all()

        db.close()
