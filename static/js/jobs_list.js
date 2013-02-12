$(function() {

    $(".run-job").click( function() {
        var job_name = $(this).parents("tr").attr("job_name");
        $.post("/job/run", { job_name : job_name }, function(data) {
            document.location.href = '/job/state';
        });
    });

    $(".remove-job").click( function() {
        var that = $(this);
        var job_name = $(this).parents("tr").attr("job_name");
        gany.modals.rusure( "Уверенны что хотите удалить задание '" + job_name + "' ?", function() {
            this.modal('hide');
            $.post("/job/remove", { job_name : job_name }, function(data) {
                if (data.status == "ok") {
                    that.parents("tr").remove();
                } else {
                    gany.modals.error("Возникла ошибка: " + data.content);
                }
            });
        });
    });

});