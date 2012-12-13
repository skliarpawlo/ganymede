from django.core.management.base import BaseCommand
from tests import tasks

class Command(BaseCommand):
    def handle(self, *args, **options):
        tasks.run_all()
