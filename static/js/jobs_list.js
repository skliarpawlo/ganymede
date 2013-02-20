$(function() {

    $(".run-job").click( function() {
        var job_id = $(this).parents("tr").attr("job_id");
        $.post("/job/run", { job_id : job_id }, function(data) {
            document.location.href = '/job/state';
        });
    });

    $(".remove-job").click( function() {
        var that = $(this);
        var job_id = $(this).parents("tr").attr("job_id");
        var job_name = $(this).parents("tr").attr("job_name");
        gany.modals.rusure( "Уверенны что хотите удалить задание #" + job_id + " '" + job_name + "'?", function() {
            this.modal('hide');
            $.post("/job/remove", { job_id : job_id }, function(data) {
                if (data.status == "ok") {
                    that.parents("tr").remove();
                } else {
                    gany.modals.error("Возникла ошибка: " + data.content);
                }
            });
        });
    });

});