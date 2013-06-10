from selenium import webdriver
import os

inst = None

errors = 0
heap = ''

def start() :
    global inst, errors
    ffb = webdriver.firefox.firefox_binary.FirefoxBinary( firefox_path = '/usr/bin/firefox' )
    # ffprofile = webdriver.firefox.firefox_profile.FirefoxProfile()
    # ffprofile.set_preference("browser.cache.disk.enable", False)
    # ffprofile.set_preference("browser.cache.memory.enable", False)
    # ffprofile.set_preference("browser.cache.offline.enable", False)
    # ffprofile.set_preference("network.http.use-cache", False)
    # inst = webdriver.Firefox( firefox_binary=ffb, firefox_profile=ffprofile )
    inst = webdriver.Firefox( firefox_binary=ffb )
    inst.implicitly_wait(5)
    inst.by_x = inst.find_element_by_xpath

def stop() :
    if not inst is None :
        inst.quit()

def setHeap( h ) :
    global heap
    heap = h

def snapshot() :
    global errors, heap, inst
    img_path = os.path.join( heap, "sc_" + str( errors ) + ".png" )
    res = inst.save_screenshot( img_path )
    if not res :
        return False
    errors += 1
    return img_path

class current_screenshot_dir:
    def __init__(self, d):
        self._dir = d

    def __enter__(self):
        global heap
        self._old_heap = heap
        heap = self._dir

    def __exit__(self, etype, value, traceback):
        global heap
        heap = self._old_heap


