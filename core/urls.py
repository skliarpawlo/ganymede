domain = u'lun.ua'

def create( subdomain=u'www', path_uri=u'' ) :
    global domain
    return u"http://" + host( subdomain ) + path(subdomain, path_uri)

def host( subdomain=u'www' ) :
    global domain
    if (domain == u'lun.ua' ) :
        return subdomain + "." + domain
    else :
        return domain

def path( subdomain=u"www", path=u"/" ) :
    global domain
    if (domain == u'lun.ua' ) :
        return path
    else :
        p = path
        if "?" in p :
            p = p + u"&domain=" + subdomain
        else :
            p = p + u"?domain=" + subdomain
        return p

