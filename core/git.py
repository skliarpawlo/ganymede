import subprocess
import json
import os
import path
import re

config = json.loads( open( os.path.abspath( os.path.dirname(__file__) ) + "/config/git.json", "r" ).read() )
path.ensure( config['repos_path'] )

def projects() :
    return config["projects"].keys()

def clone(project) :
    with path.cd( os.path.join( config['repos_path'] ) ) :
        subprocess.call( [ "git", "clone", config[ 'projects' ][ project ][ 'repo' ] ] )

def branches(project) :
    working_dir = os.path.join( config['repos_path'], project )
    if not os.path.exists(working_dir) :
        clone(project)

    with path.cd( working_dir ) :
        pipe = subprocess.Popen( ["git", "branch", "-r"], stdout=subprocess.PIPE )
        res = pipe.stdout.read()
        brs = re.findall("t[0-9]+-[a-zA-Z]+", res)

    return brs

def checkout_and_deploy(project, branch) :
    working_dir = os.path.join( config['repos_path'], project )
    if not os.path.exists(working_dir) :
        clone(project)

    with path.cd( working_dir ) :
        subprocess.call( ["git", "checkout", branch] )
        subprocess.call( ["git", "pull", "--rebase"] )

        subprocess.call( ["rm -rf " + os.path.join( config['deploy_path'], "*" ) ], shell = True )
        subprocess.call( ["cp -rf * " + config['deploy_path']], shell = True )

        subprocess.call( ["rm", "-rf", os.path.join( config['deploy_path'], ".git" ) ] )

        subprocess.call( ["mkdir", os.path.join( config['deploy_path'], "assets" ) ] )
        subprocess.call( ["chmod", "777", os.path.join( config['deploy_path'], "assets" ) ] )
        subprocess.call( ["mkdir", os.path.join( config['deploy_path'], "protected", "runtime" ) ] )
        subprocess.call( ["chmod", "777", os.path.join( config['deploy_path'], "protected", "runtime" ) ] )
