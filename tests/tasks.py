from celery import task
import unittest
import tests

@task()
def add(x, y):
    logger = add.get_logger()
    logger.info("xxx fake task xxx");
    return x + y

@task()
def run_test():

    t = tests.CheckRedirectTestCase()
    t.setUp()
    t.
    t.tearDown()
