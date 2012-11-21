from celery import task
import unittest
import tests

@task()
def add(x, y):
    logger = add.get_logger()
    logger.info("xxx fake task xxx")
    return x + y

@task()
def run_test():
    t = tests.CheckSeoTextsTestCase()
    success = True
    try :
        t.setUp()
        t.run()
    except :
        success = False
    finally:
        t.tearDown()
    return success
