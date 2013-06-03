import subprocess
import logger
import time

def get_output( proc ) :
    pipe = subprocess.Popen( proc, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
    return pipe.stdout.read()

def output_to_log( proc, **wargs ) :
    pipe = subprocess.Popen( proc, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **wargs )

    while pipe.poll() is None :
        out = pipe.stdout.readline()
        if (len(out) > 0) :
            logger.write( out.decode("utf-8").rstrip() )
    ###
    out = pipe.stdout.read()
    if (len(out) > 0) :
        logger.write( out.decode("utf-8").rstrip() )
