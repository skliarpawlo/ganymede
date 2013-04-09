import subprocess
import logger

def get_output( proc ) :
    pipe = subprocess.Popen( proc, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
    return pipe.stdout.read()

def output_to_log( proc, **wargs ) :
    pipe = subprocess.Popen( proc, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **wargs )
    out = pipe.stdout.read()
    if (len(out) > 0) :
        logger.write( out.decode("utf-8") )
    err = pipe.stderr.read()
    if (len(err) > 0) :
        logger.write( err.decode("utf-8") )
