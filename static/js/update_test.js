$(function() {
    $("#update-test-btn").click( function() {
        var params = gany.test.gather_data();
        // submit
        $.post("",params).done( function(data) {
            if (data.status == "ok") {
                gany.modals.info(gettext('Changes saved'));
            } else {
                gany.modals.error(gettext('Error occured') + ": " + data.content);
            }
        });
    });

    $("#test-tag-list").tags( {
        tagData : tags
    } );

});