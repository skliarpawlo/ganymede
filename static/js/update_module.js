$( function() {

    $( "#update-module-btn").click( function() {
        $.post( "", gany.modules.gather_data(), function( data ) {
            if (data.status == "ok") {
                gany.modals.info(gettext('Changes saved'));
            } else {
                gany.modals.error(gettext('Error occured') + ": " + data.content);
            }
        } )
    } );

} );