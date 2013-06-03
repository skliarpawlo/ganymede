$(function(){

    log_size = 0;
    results_count = 0;
    current_test_log_size = 0;

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

    $(document).delegate( ".show-log", "click", function() {
        gany.modals.info( $(this).siblings(".log").html().split("\n").join("<br/>") );
    });

    $(document).bind("data-appended", function() {
        $("#result-table").show();
        $('[data-toggle="tooltip"]').tooltip();
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
                "<a data-toggle='tooltip' data-original-title='" + gettext('View') + "' href='/test/update/${test_id}'><i class='icon-file' title='" + gettext('Test') + "' /></a>" +
                "<a data-toggle='tooltip' data-original-title='" + gettext('Log') + "' class='show-log cursor-hand'>" +
                    "<i class='icon-tasks' title='" + gettext('Log') + "' />" +
                "</a>" +
                "<div class='log'>{{html log}}</div>" +
                "{{each artifacts}}" +
                    "<a data-toggle='tooltip' data-original-title='" + gettext('Screenshot') + "' class='fancybox' rel='group1' href='${$value.path}'><i class='icon-picture' /></a>" +
                "{{/each}}" +
            "</td>" +
        "</tr>";

    var current_markup =
        "<tr class='test-result-row current-running'>" +
            "<td>" +
                "<span class='label label-info'>Running</span>" +
                "<img src='/static/images/progress.gif'/>" +
            "</td>" +
            "<td>${name}</td>"+
            "<td>" +
                "<a data-toggle='tooltip' data-original-title='" + gettext('View') + "' href='/test/update/${test_id}'><i class='icon-file' title='" + gettext('Test') + "' /></a>" +
                "<a data-toggle='tooltip' data-original-title='" + gettext('Log') + "' class='show-log cursor-hand'>" +
                    "<i class='icon-tasks' title='" + gettext('Log') + "' />" +
                "</a>" +
                "<div class='log' id='current-test-log'>{{html log}}</div>" +
                    "{{each artifacts}}" +
                        "<a data-toggle='tooltip' data-original-title='" + gettext('Screenshot') + "' class='fancybox' rel='group1' href='${$value.path}'><i class='icon-picture' /></a>" +
                    "{{/each}}" +
            "</td>" +
        "</tr>";

    $.template( "result_markup", result_markup );
    $.template( "current_markup", current_markup );

    var log_block = gany.code.block("log-block", {
        mode : {
            name : "shell"
        },
        lineNumbers : true,
        readOnly : true
    });

    // stupid hack to force redraw
    $(".nav-tabs li").click(function(){
        setTimeout( function() {
            log_block.refresh();
        }, 500);
    });


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

    var AJAX_LOCK = false;

    var log_func = function() {

        if (AJAX_LOCK) return; AJAX_LOCK = true;

        gany.task.log( taskId, log_size, results_count, current_test_log_size ).done( function(data) {
            if (data.status == "ok") {
                results_count += data.content.result.length;
                log_size += data.content.text.length;

                if ( data.content.current != false ) {
                    if ( data.content.current.state == 'new' ) {
                        current_test_log_size = 0
                    }
                    current_test_log_size += data.content.current.log.length;
                    data.content.current.log = process_diffs(data.content.current.log);
                }

                for ( x in data.content.result ) {
                    data.content.result[ x ].log = process_diffs(data.content.result[ x ].log);
                }

                $("#log-block").html($("#log-block").html() + data.content.text);
                gany.code.block("log-block").setValue( $("#log-block").html() );

                $.tmpl( "result_markup", data.content.result)
                    .css("display", "none")
                    .appendTo("#result-data")
                    .fadeIn(360);

                if ( data.content.current != false ) {
                    if ( data.content.current.state == 'new' ||
                        $("#result-data").find(".current-running").size() == 0 ) {
                        $("#result-data")
                            .find(".current-running")
                            .remove();
                        $.tmpl( "current_markup", data.content.current)
                            .css("display", "none")
                            .appendTo("#result-data")
                            .fadeIn(0);
                    } else {
                        $("#current-test-log").append( data.content.current.log );
                    }
                }

                if (data.content.state == "final") {
                    $("#result-data").find(".current-running").remove();
                    $("#stop-task").hide();
                    $(".log-loader").hide();
                    clearInterval(t);
                }
                $(document).trigger( "data-appended" );
            }
            AJAX_LOCK = false;
        });
    };
    var t = setInterval( log_func, 1200 );
    log_func();

    $("#stop-task").click( function() {
        gany.task.stop_current_task()
    } );

});