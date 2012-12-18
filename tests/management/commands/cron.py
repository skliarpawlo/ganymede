from django.core.management.base import BaseCommand
from tests import tasks
from core import db
from core import mode

class Command(BaseCommand):
    def handle(self, *args, **options):
        db.init()
        mode.set_mode( mode.PRODUCTION )
        mode.set_completeness( mode.COMPLETENESS_FULL )

        tasks.run_all()

        db.close()
