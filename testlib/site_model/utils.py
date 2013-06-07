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
