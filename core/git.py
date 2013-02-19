import json
import os
import path
import re
import logger
import process
import ganymede.settings

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

    with path.cd( working_dir ) :
        res = process.get_output( ["git", "branch", "-r"] )
        brs = re.findall("t[0-9]+-[a-zA-Z\-]+", res)

    brs.append('master')
    brs.append('develop')

    return brs

def checkout_and_deploy(job) :
    project = job.repo
    branch = job.branch
    env = job.env

    working_dir = os.path.join( config['repos_path'], project )
    if not os.path.exists(working_dir) :
        clone(project)

    with path.cd( working_dir ) :
        process.output_to_log( ["git", "checkout", branch] )
        process.output_to_log( ["git", "fetch"] )
        process.output_to_log( ["git", "reset", "--hard", "origin/" + branch] )

        process.output_to_log( ["rm -rf " + os.path.join( config['deploy_path'], "*" ) ], shell = True )
        process.output_to_log( ["cp -rf * " + config['deploy_path']], shell = True )

        process.output_to_log( ["rm", "-rf", os.path.join( config['deploy_path'], ".git" ) ] )

        process.output_to_log( ["mkdir", os.path.join( config['deploy_path'], "assets" ) ] )
        process.output_to_log( ["chmod", "777", os.path.join( config['deploy_path'], "assets" ) ] )
        process.output_to_log( ["mkdir", os.path.join( config['deploy_path'], "protected", "runtime" ) ] )
        process.output_to_log( ["chmod", "777", os.path.join( config['deploy_path'], "protected", "runtime" ) ] )

        #env
        fd = open( os.path.join( config['deploy_path'], "environment.php" ), 'w' )
        fd.write( env )
        fd.close()
