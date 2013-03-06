$(function(){

    log_size = 0;
    results_count = 0;

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

    $(document).bind("data-appended", function() {
        $(".show-log").unbind("click").bind( "click", function() {
            gany.modals.info( $(this).next().html().split("\n").join("<br/>") );
        });
    });

    $("#toggle-task-log").click(function(){
        $("#log-block").toggle();
    });

    var result_markup =
        "<tr class='test-result-row'>" +
            "<td>" +
                "{{if status=='success'}}" +
                    "<span class='label label-success'>Success</span>" +
                "{{else}}" +
                    "<span class='label label-important'>Fail</span>" +
                "{{/if}}" +
            "</td>" +
            "<td>${name}</td>"+
            "<td>" +
                "<a href='/test/update/${test_id}'><i class='icon-file' title='test' /></a>" +
                "<a href='#' class='show-log'>" +
                    "<i class='icon-tasks' title='log' />" +
                "</a>" +
                "<div class='log'>{{html log}}</div>" +
                "{{each artifacts}}" +
                    "<a href='${$value.path}' title='screenshot'><i class='icon-picture' /></a>" +
                "{{/each}}" +
            "</td>" +
        "</span>";

    $.template( "result_markup", result_markup );

    var process_diffs = function( data ) {
        var res = $("<div>" + data + "</div>");
        var diff_blocks = res.find(".textdiff");
        diff_blocks.each( function( ind, el ) {
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
        gany.task.log( taskId, log_size, results_count ).done( function(data) {
            if (data.status == "ok") {
                results_count += data.content.result.length;
                log_size += data.content.text.length;

                data.content.text = process_diffs(data.content.text);
                $("#log-block").html($("#log-block").html() + data.content.text.split("\n").join("<br/>"));

                $.tmpl( "result_markup", data.content.result).css("display", "none").appendTo("#result-data").fadeIn(360);

                if (data.content.state == "final") {
                    $("#stop-task").hide();
                    $(".log-loader").hide();
                    clearInterval(t);
                }
                $(document).trigger( "data-appended" );
            }
        });
    };
    var t = setInterval( log_func, 1200 );
    log_func();

    $("#stop-task").click( function() {
        gany.task.stop_current_task()
    } );

});