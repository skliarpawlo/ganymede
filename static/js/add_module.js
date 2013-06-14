$( function() {

    $( "#сreate-module-btn").click( function() {
        $.post( "", gany.modules.gather_data(), function( data ) {
            if (data.status == "ok") {
                gany.modals.info(gettext('Module added'));
            } else {
                gany.modals.error(gettext('Error occured') + ": " + data.content);
            }
        } )
    } );

} );