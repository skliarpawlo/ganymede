from selenium import webdriver
import os

inst = None

errors = 0
heap = ''

def start() :
    global inst
    ffb = webdriver.firefox.firefox_binary.FirefoxBinary( firefox_path = '/usr/bin/firefox' )
    inst = webdriver.Firefox( firefox_binary=ffb )

def stop() :
    if not inst is None :
        inst.quit()

def setHeap( h ) :
    global heap
    heap = h

def save() :
    global errors, heap, inst
    inst.save_screenshot( os.path.join( heap, "sc_" + str( errors ) + ".png" ) )
    errors += 1
