$(function(){

    log_size = 0;

    $(".fancybox").fancybox({
        fitToView : false,
        helpers: {
            title : {
                type : 'inside'
            },
            thumbs : {
                width: 50,
                height: 50
            }
        }
    });

    var artefact_markup =
        "<span class='fancy-boxed'>" +
            "<a title='${source}' class='fancybox' rel='group' href='${path}'>" +
                "<img class='fancy-boxed' src='${path}' />" +
            "</a>" +
        "</span>";

    $.template( "artefact_markup", artefact_markup );

    var log_func = function() {
        gany.task.log( taskId, log_size, $("#artifacts-block .fancybox").size() ).done( function(data) {
            if (data.status == "ok") {
                log_size += data.content.text.length;
                $("#log-block").html($("#log-block").html() + data.content.text.split("\n").join("<br/>"));
                $.tmpl( "artefact_markup", data.content.artifacts).css("display", "none").appendTo("#artifacts-block").fadeIn(1300);
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