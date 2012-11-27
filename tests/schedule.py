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

def run_all() :
    for x in tests_config.all_tests:
        run(x)

if (__name__=="__main__"):
    run_all()