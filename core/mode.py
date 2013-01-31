# coding: utf-8
DEBUG = 'debug'
PRODUCTION = 'silent'

mode = PRODUCTION

def set_mode( _mode ) :
    "Задание режима 'silent' - для web части, 'debug' - для дебага"
    global mode
    mode = _mode

testcase = '*'
def set_testcase( _testcase ) :
	global testcase
	testcase = _testcase