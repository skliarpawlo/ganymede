$( function() {

    function performRequest(test_id, op_id) {
        return $.ajax( {
            type : "GET",
            url : "/ajax/test",
            data : {
                test_id : test_id,
                op_id : op_id,
                domain: $("#domain-val").val()
            }
        })
    }

    $(".test-start-btn").click( function() {
        var test_id = $(this).parents("[test_id]").attr("test_id");
        var op_id = 'test';
        performRequest(test_id, op_id).done( function(data) {
            $("#info-message").html(data.message);
            $("#info-modal").modal();
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

    $("#test-all").click(function(){
        var test_id = '__test_all__';
        var op_id = 'test';
        performRequest(test_id, op_id).done( function(data) {
            $("#info-message").html(data.message);
            $("#info-modal").modal();
        });
    });

    ////

    $("a[rel=popover]").each(function(ind,el){
        var that = $(el);
        that.popover( {
            title:"Предназначение теста",
            content:that.siblings(".doc").text(),
            delay: { show: 500, hide: 100 }
        } );
    });

    $("#domain-val").keypress( function(e) {
        if (e.keyCode == 13)
            document.location = "?domain=" + $("#domain-val").val();
    });

} );