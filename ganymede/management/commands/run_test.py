from django.core.management.base import BaseCommand
import unittest

class Command(BaseCommand):
    def handle(self, *args, **options):
        mod = __import__('tests.tests', globals(), locals(), [], -1)
        unittest.main(module=)

if (__name__=='__main__'):
    c = Command()
    c.handle()