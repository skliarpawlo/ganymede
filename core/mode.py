# coding: utf-8
DEBUG = 'debug'
PRODUCTION = 'silent'

mode = 'silent'

def set( _mode ) :
    "Задание режима 'silent' - для web части, 'debug' - для дебага"
    global mode
    mode = _mode