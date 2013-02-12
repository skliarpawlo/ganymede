$( function() {

    var verifyData = function (data) {
        var errors = [];
        if (data.name == '')
            errors.push( "Имя не может быть пустым" );
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
                    gany.modals.info("Задание созданно").bind("hidden", function() {
                        document.location.href = "/job/list";
                    });
                } else {
                    gany.modals.error("Возникла ошибка: " + data.content);
                }
            });
        } else {
            gany.boxes.error($("#create-job-error")).show(errors);
        }
    });

} );