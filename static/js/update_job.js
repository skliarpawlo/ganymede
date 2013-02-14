$(function() {

    $("#update-job-btn").click( function() {
        var params = gany.job.gather_data();
        // submit
        $.post("",params).done( function(data) {
            if (data.status == "ok") {
                gany.modals.info("Изменения сохранены");
            } else {
                gany.modals.error("Возникла ошибка: " + data.content);
            }
        });
    });

});