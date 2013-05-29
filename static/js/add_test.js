$(function(){

    $("#сreate-test-btn").click(function() {
        var data = gany.test.gather_data();
        $.post("", data).done(function(data) {
            if (data.status == "ok") {
                gany.modals.info( gettext('Test was successfully added') );
            } else {
                gany.modals.error(gettext('Error occured') + ": " + data.content);
            }
        });
    });

    $("#test-tag-list").tags();

});