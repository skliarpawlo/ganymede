import MySQLdb

_host="77.120.117.134" #"127.0.0.1"
_dbname="lun_ua_new"
_user="skliar"
_passwd="lilipad"

con = None

def connect() :
    global con
    con = MySQLdb.connect( host=_host, db=_dbname, user=_user, passwd=_passwd )

def close() :
    if not con is None :
        con.close()
        
def createCommand( sql ) :
    class SqlCommand :
        def queryAll( self ) :
            cursor = con.cursor( MySQLdb.cursors.DictCursor )
            cursor.execute("SET NAMES utf8")
            cursor.execute( sql )
            return cursor.fetchall()
        def execute( self ) :
            cursor = con.cursor( MySQLdb.cursors.DictCursor )
            cursor.execute("SET NAMES utf8")
            cursor.execute( sql )
    command = SqlCommand()
    return command
        
if ( __name__ == "__main__" ) :
    connect()
    cmd = createCommand( 'SELECT * FROM buildings limit 5' )
    res = cmd.queryAll()
    for x in res :
        print( x )
        
