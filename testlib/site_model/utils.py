def hack_ajax(ff) :
    ff.execute_script( """
       $.ajax = function() {
           var def = $.Deferred();
           document.ganymede_last_sent_ajax = arguments[0].data;
           def.resolve( "ok" );
           if (arguments[0].success) {
              def.done( arguments[0].success );
           }
           return def;
       }
    """ )


def element_present( ff, x ) :
    try :
        ff.by_x( x )
        res = True
    except :
        res = False
    return res


def merge( a, b, path=None ):
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a
