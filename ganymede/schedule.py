import sched
import time

scheduler = sched.scheduler(time.time, time.sleep)

def temp(name):
    print("temp event occured with arg {0}".format(name))

scheduler.enter(2, 1, temp, ('xxx',))
scheduler.enter(3, 1, temp, ('yyy',))

scheduler.run()