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

    var process_diffs = function( data ) {
        var res = $("<div>" + data + "</div>");
        var diff_blocks = res.find(".textdiff");
        diff_blocks.each( function( ind ,el ) {
            var t1 = $(el).find(".base").text();
            var t2 = $(el).find(".changed").text();

            tableBody = document.createElement('table');
            $(el).replaceWith($(tableBody));
            diff_tool.setTableElement(tableBody);
            diff_tool.clearTableBody();
            diff_tool.diff(t1.split('\n'), t2.split('\n'));

        } );
        return res.html();
    }

    var log_func = function() {
        gany.task.log( taskId, log_size, $("#artifacts-block .fancybox").size() ).done( function(data) {
            if (data.status == "ok") {
                log_size += data.content.text.length;
                data.content.text = process_diffs(data.content.text);
                $("#log-block").html($("#log-block").html() + data.content.text.split("\n").join("<br/>"));
                $.tmpl( "artefact_markup", data.content.artifacts).css("display", "none").appendTo("#artifacts-block").fadeIn(1300);
                if (data.content.state == "final") {
                    $("#log-loader").hide();
                    $("#log-loader-bottom").hide();
                    clearInterval(t);
                }
            }
        });
    };
    var t = setInterval( log_func, 1200);
    log_func();

});