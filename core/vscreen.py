from pyvirtualdisplay import Display
from ganymede import settings

display = None

def start() :
    global display
    if not settings.USE_VSCREEN :
        return
    if display is None :
        display = Display( visible = 0, size=( 1200, 800 ) )
    display.start()
        
def stop() :
    if not settings.USE_VSCREEN :
        return
    if not display is None :
        display.stop()

