$( function() {

    var verifyData = function (data) {
        var errors = [];
        if (data.name == '')
            errors.push( gettext('Name cannot be empty') );
        return errors;
    };

    $("#сreate-job-btn").click( function() {
        var data = gany.job.gather_data();

        var errors = verifyData(data);
        if ( errors.length == 0 ) {
            // submit
            var defered = $.post("/job/create",data);
            defered.done( function(data) {
                if (data.status == "ok") {
                    gany.modals.info(gettext('Job created')).bind("hidden", function() {
                        document.location.href = "/job/list";
                    });
                } else {
                    gany.modals.error(gettext('Error occured') + ": " + data.content);
                }
            });
        } else {
            gany.boxes.error($("#create-job-error")).show(errors);
        }
    });

} );