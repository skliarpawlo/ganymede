$( function() {

    $("#сreate-job-btn").click( function() {
        var data = gany.job.gather_data();
        // submit
        $.post(
            "/job/create",
            data,
            function(data) {
                var ans = $.parseJSON(data);
                console.log(ans);
            }
        );
    });

} );