import tests_config
import utils

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

    # save result
    fd = open(utils.res_file(test_id), 'w')
    if (success) :
        fd.write('ACCEPTED')
    else :
        fd.write('FAILED')
    fd.close()

    return success
