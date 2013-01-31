import imp
import glob, inspect
import utils

all_tests = {}
sub_tests = {}

# search for tests ing tests_root dir
for test_path in glob.glob("tests_root/**/*.py"):
    if test_path[-11:] == "__init__.py":
        continue
    try:
        mod_name = ".".join( test_path.split("/") )[:-3]
        mod = imp.load_source( mod_name, test_path )
        for name, obj in inspect.getmembers( mod ) :
            # page tests
            if (inspect.isclass(obj)) and (obj.__module__ == mod_name) and issubclass(obj, utils.PageTest) :
                all_tests[ mod_name ] = obj()

            # subtests
            if (inspect.isclass(obj)) and (obj.__module__ == mod_name) and issubclass(obj, utils.SubTest) :
                if not sub_tests.has_key(mod_name) :
                    sub_tests[ mod_name ] = []
                sub_tests[ mod_name ].append(obj())

        # attaching subtests
        for x in sub_tests :
            for subtest in sub_tests[x] :
                all_tests[ x ].addSubtest( subtest )

    except ImportError, m :
        print "Error while importing %s - %s"%(test_path,m)

#
#TODO: search for tests in db
#