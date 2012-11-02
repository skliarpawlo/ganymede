import re

def remove_new_lines( txt ) :
    return " ".join( txt.splitlines() )
        
def remove_html_tags( data ):
    p = re.compile( r'<.*?>' )
    return p.sub( '', data )        
