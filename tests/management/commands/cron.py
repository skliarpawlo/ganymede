from django.core.management.base import BaseCommand
from tests import tasks
from core import db
from core import mode
from core import urls

class Command(BaseCommand):
    def handle(self, domain='lun.ua', testcase='**', *args, **options):
        urls.domain = domain
        mode.set_testcase( testcase )
        mode.set_mode( mode.PRODUCTION )
        mode.set_completeness( mode.COMPLETENESS_FULL )

        db.init()

        tasks.run_all()

        db.close()
