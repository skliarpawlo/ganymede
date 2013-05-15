from pyvirtualdisplay import Display

display = None

def start() :
    global display
    if display is None :
        display = Display( visible = 0, size=( 800, 600 ) )
    display.start()
        
def stop() :
    if not display is None :
        display.stop()

