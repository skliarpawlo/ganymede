# coding: utf-8
DEBUG = 'debug'
PRODUCTION = 'silent'

mode = PRODUCTION

def set_mode( _mode ) :
    "Задание режима 'silent' - для web части, 'debug' - для дебага"
    global mode
    mode = _mode

COMPLETENESS_FULL = 'full'
COMPLETENESS_FAST = 'fast'

complete = COMPLETENESS_FULL
def set_completeness( _compl ) :
    "Задание полноты тестирования 'full' - полное, 'fast' - быстрое"
    global complete
    complete = _compl