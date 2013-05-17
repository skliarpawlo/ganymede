import json
import os
import path
import re
import logger
import process
import ganymede.settings
import subprocess
import stat

config = json.loads(
    open(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "config",
            ganymede.settings.MODE,
            "git.json"
        ),
        "r" ).read()
)
path.ensure( config['repos_path'] )

def projects() :
    return config["projects"].keys()

def clone(project) :
    with path.cd( os.path.join( config['repos_path'] ) ) :
        out = process.get_output([ "git", "clone", config[ 'projects' ][ project ][ 'repo' ] ])
        logger.write( out )

def fetch(project) :
    working_dir = os.path.join( config['repos_path'], project )
    if not os.path.exists(working_dir) :
        clone(project)
    res = 'empty'
    with path.cd( working_dir ) :
        res = process.get_output( [ "git", "fetch" ] )
    return res

def branches(project) :
    working_dir = os.path.join( config['repos_path'], project )
    if not os.path.exists(working_dir) :
        clone(project)

    result = []
    with path.cd( working_dir ) :
        res = process.get_output( ["git", "branch", "-r"] )
        brs = re.findall("origin/[\w\-]+", res)
        for x in brs :
            result.append(x[7:])

    result.append('master')
    result.append('develop')

    return result

def checkout_and_deploy(job) :
    project = job.repo
    branch = job.branch
    envs = job.envs
    deploy_code = job.deploy

    working_dir = os.path.join( config['repos_path'], project )
    if not os.path.exists(working_dir) :
        clone(project)

    # deploy
    if not deploy_code is None :
        # create deploy script file
        tmp_dir = os.path.join( ganymede.settings.HEAP_PATH, "tmp" )
        path.ensure( tmp_dir )
        deploy_script = os.path.join( tmp_dir, "temp_deploy.sh" )
        fd = open( deploy_script, 'w' )
        fd.write( deploy_code )
        fd.close()

        os.chmod( deploy_script, 0777 )

        # form env
        environ = {
            "REPO" : job.repo,
            "BRANCH" : job.branch,
            "PROJECT_PATH" : working_dir,
            "DEPLOY_PATH" : config['deploy_path'],
        }

        # execute it
        process.output_to_log( deploy_script, env=environ, shell=True )

        os.unlink( deploy_script )

    #envs
    for env in envs :
        fd = open( os.path.join( config['deploy_path'], env.path ), 'w' )
        fd.write( env.code.encode("utf-8") )
        fd.close()
