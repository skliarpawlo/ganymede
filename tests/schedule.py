import sched
import time
import tests_config
import utils
import tasks
import core.lock

def run(test_id) :
    pid_file = utils.pid_file(test_id)
    test_pid = core.lock.is_free(pid_file)
    if (test_pid==0):
        core.lock.capture(pid_file)
        tasks.run_test(test_id)
        core.lock.uncapture(pid_file)


scheduler = sched.scheduler(time.time, time.sleep)

for x in tests_config.all_tests:
    scheduler.enter(1, 1, run, (x,))

scheduler.run()