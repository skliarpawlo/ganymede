domain = u'lun.ua'

def create( subdomain=u'www', path=u'' ) :
    global domain
    if (domain == u'lun.ua' ) :
        return u"http://" + subdomain + "." + domain + path
    else :
        p = u"http://" + domain + path
        if "?" in p :
            p = p + u"&domain=" + subdomain
        else :
            p = p + u"?domain=" + subdomain
        return p

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

