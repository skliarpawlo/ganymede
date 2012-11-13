$( function() {

    function performRequest(test_id, op_id) {
        return $.ajax( {
            type : "GET",
            url : "/ajax/test",
            data : { test_id : test_id, op_id : op_id }
        })
    }

    $(".test-start-btn").click( function() {
        var test_id = $(this).parents("[test_id]").attr("test_id");
        var op_id = 'test';
        performRequest(test_id, op_id).done( function(data) {
        });
    });

    $(".test-log-btn").click( function() {
        var test_id = $(this).parents("[test_id]").attr("test_id");
        var op_id = 'log';
        performRequest(test_id, op_id).done( function(data) {
            if (data.status == 0) {
                $("#log-message").html(data.message);
                $("#log-modal").modal();
            } else {
                $("#error-message").html(data.message);
                $("#error-modal").modal();
            }
        });
    });

} );