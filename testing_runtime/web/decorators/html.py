def link( url, title ) :
    return u"<a target='_blank' href='{0}'>{1}</a>".format(url, title)

def status_label( status, title ) :
    if status == 'fail' :
        return u'<span class="label label-important">{0}</span>'.format(title)
    else :
        return u'<span class="label label-success">{0}</span>'.format(title)

def diff( text1, text2 ) :
    return u"<span class='textdiff'> <span class='base'>{0}</span> <span class='changed'>{1}</span> </span>".format( text1, text2 )