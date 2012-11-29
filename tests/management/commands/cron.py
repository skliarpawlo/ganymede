from django.core.management.base import BaseCommand
from tests import schedule

class Command(BaseCommand):
    def handle(self, *args, **options):
        schedule.run_all()
