import tests_config
import utils
import core.urls

def run_test(test_id):
    t_class = tests_config.all_tests[test_id]
    t = t_class(test_id)
    success = True
    try :
        t.setUp()
        t.run()
    except AssertionError:
        success = False
    except Exception as s :
        print "ERROR: ", s
        success = False
    finally:
        t.tearDown()

    # save result
    fd = open(utils.res_file(test_id), 'w')
    if (success) :
        fd.write('ACCEPTED [{0}]'.format(core.urls.domain))
    else :
        fd.write('FAILED [{0}]'.format(core.urls.domain))
    fd.close()

    return success
