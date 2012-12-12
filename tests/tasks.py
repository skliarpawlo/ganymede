import tests_config
from models import TestResult
from core import db
import core.urls
import traceback
import sys
import codecs
from cStringIO import StringIO

def run_test(test_id):
    t_class = tests_config.all_tests[test_id]
    t = t_class(test_id)

    success = True

    # redirect to log
    _err = sys.stderr
    _out = sys.stdout
    sys.stderr = sys.stdout = StringIO()
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)
    sys.stderr = codecs.getwriter('utf8')(sys.stderr)

    try :
        t.setUp()
        t.run()
    except AssertionError:
        success = False
    except Exception as s :
        print "ERROR: ", s
        print traceback.format_exc()
        success = False
    finally:
        t.tearDown()

        log = sys.stdout.getvalue()

        sys.stdout.close()
        sys.stderr.close()

        sys.stdout = _out
        sys.stderr = _err

        # save result
        status = ''
        if (success) :
            status = 'ACCEPTED [{0}]'.format(core.urls.domain)
        else :
            status = 'FAILED [{0}]'.format(core.urls.domain)

        res = TestResult( test_id=test_id, domain=core.urls.domain, status=status, log=log )
        db.session.add(res)
        db.session.commit()

    return success
