import os

def is_free(pid_file):
    "Checks if pid file is free. Returns 0 if it is free, otherwise pid of using process"
    if os.access(pid_file, os.F_OK):
        pidf = open(pid_file, "r")
        pidf.seek(0)
        old_pid = pidf.readline()
        pidf.close()
        if os.path.exists("/proc/{0}".format(old_pid)) and not (old_pid==os.getpid()):
            return old_pid
        else:
            return 0
    else :
        return 0

def uncapture(pid_file) :
    os.unlink(pid_file)

def capture(pid_file):
    pidf = open(pid_file, "w")
    pidf.write("{0}".format(os.getpid()))
    pidf.close()
    os.chmod(pid_file, 0777)