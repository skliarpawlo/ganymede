$(function(){

    var log_func = function() {
        gany.task.log( taskId, $("#log-block").text().length ).done( function(data) {
            if (data.status == "ok") {
                $("#log-block").text($("#log-block").text() + data.content.text);
                if (data.content.state == "final") {
                    $("#log-loader").hide();
                    clearInterval(t);
                }
            }
        });
    };
    var t = setInterval( log_func, 1200);
    log_func();

});