import os

STATUS_SUCCESS = 1
STATUS_FAIL = 2

def capture(pid_file):
    if os.access(pid_file, os.F_OK):
        pidf = open(pid_file, "r")
        pidf.seek(0)
        old_pid = pidf.readline()
        pidf.close()
        if os.path.exists("/proc/{0}".format(old_pid)) and not (old_pid==os.getpid()):
            return STATUS_FAIL
        else:
            _perform_capture(pid_file)
            return STATUS_SUCCESS
    else :
        _perform_capture(pid_file)
        return STATUS_SUCCESS

def uncapture(pid_file) :
    os.unlink(pid_file)

def _perform_capture(pid_file):
    pidf = open(pid_file, "w")
    pidf.write("{0}".format(os.getpid()))
    pidf.close()