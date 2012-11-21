from celery import task
import tests_config

@task()
def add(x, y):
    logger = add.get_logger()
    logger.info("xxx fake task xxx")
    return x + y

@task()
def run_test(test_id):
    t_class = tests_config.all_tests[test_id]
    t = t_class(test_id)
    success = True
    try :
        t.setUp()
        t.run()
    except :
        success = False
    finally:
        t.tearDown()
    return success
