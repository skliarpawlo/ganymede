#!/usr/bin/env python
from tests import schedule
from sys import argv
import ganymede.settings
ganymede.settings.DEBUG = True
if len(argv) == 1:
    print "./debug.py <test>"
else:
    schedule.run(argv[1])