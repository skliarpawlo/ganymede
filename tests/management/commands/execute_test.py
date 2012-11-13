from django.core.management.base import BaseCommand
import unittest
import sys

sys.path.append( "./../../.." )

class Command(BaseCommand) :
    def handle(self, *args, **options):
        test_id = args[0]
        print(test_id)
        unittest.main(module='tests.' + test_id + '.test_' + test_id)

if (__name__=='__main__'):
    c = Command()
    c.handle('seo_texts')