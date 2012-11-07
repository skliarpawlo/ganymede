import os
import ganymede.settings

heap_dir = ganymede.settings.HEAP_PATH
base_dir = ganymede.settings.BASE_PATH

def test_dir(test_id) :
    return os.path.join(heap_dir, "tests", test_id)

def test_exe(test_id) :
    return os.path.join(base_dir, "tests", test_id, test_id + ".py")

def photos_dir(test_id) :
    return os.path.join(test_dir(test_id), "photos")
