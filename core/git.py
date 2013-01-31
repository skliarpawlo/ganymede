import subprocess
import json
import os
import path

config = json.loads( open( os.path.abspath( os.path.dirname(__file__) ) + "/config/git.json", "r" ).read() )
path.ensure( config['repos_path'] )

def _clone() :
    with path.cd( os.path.join( config['repos_path'] ) ) :
        subprocess.call( [ "git", "clone", config[ project ][ 'repo' ] ] )

project = "callisto"

def set_project( proj ) :
    global project
    project = proj

def checkout_and_deploy(branch) :
    working_dir = os.path.join( config['repos_path'], project )
    if not os.path.exists(working_dir) :
        _clone()

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
