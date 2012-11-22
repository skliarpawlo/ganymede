import sched
import time
from tests import tests_config
from tests import tasks

scheduler = sched.scheduler(time.time, time.sleep)

for x in tests_config.all_tests:
    scheduler.enter(1, 1, tasks.run_test, (x,))

scheduler.run()