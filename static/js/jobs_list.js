$(function() {

    $(".run-job").click( function() {
        var job_name = $(this).parents("tr").attr("job_name");
        $.post("/job/run", { job_name : job_name }, function(data) {
            var ans = $.parseJSON(data);
            document.location.href = '/job/state';
        });
    });

    $(".remove-job").click( function() {
        var job_name = $(this).parents("tr").attr("job_name");
        gany.modals.rusure.show( "Уверенны что хотите удалить задание '" + job_name + "' ?", function() {
            $.post("/job/remove", { job_name : job_name }, function(data) {
                var ans = $.parseJSON(data);
            });
        });
    });

});