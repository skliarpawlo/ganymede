domain = 'lun.ua'

def create( subdomain='www', path='' ) :
    global domain
    if (domain == 'lun.ua' ) :
        return "http://" + subdomain + "." + domain + path
    else :
        p = "http://" + domain + path
        if "?" in p :
            p = p + "&domain=" + subdomain
        else :
            p = p + "?domain=" + subdomain
        return p

def host( subdomain='www' ) :
    global domain
    if (domain == 'lun.ua' ) :
        return subdomain + "." + domain
    else :
        return domain

def path( subdomain="www", path = "/" ) :
    global domain
    if (domain == 'lun.ua' ) :
        return path
    else :
        p = path
        if "?" in p :
            p = p + "&domain=" + subdomain
        else :
            p = p + "?domain=" + subdomain
        return p

