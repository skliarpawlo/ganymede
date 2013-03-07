def link( url, title ) :
    return u"<a target='_blank' href='{0}'>{1}</a>".format(url, title)

def status_label( status ) :
    if status == 'fail' :
        return u'<span class="label label-important">Fail</span>'
    else :
        return u'<span class="label label-success">Success</span>'

def diff( text1, text2 ) :
    return u"<span class='textdiff'> <span class='base'>{0}</span> <span class='changed'>{1}</span> </span>".format( text1, text2 )

def title( l ) :
    return " - ".join( l )