import os
import sys

def daemonize() :
    pid = os.fork()
    if (pid < 0):
        raise Exception('Fork failed')
    if (pid > 0):
        sys.exit(0)
