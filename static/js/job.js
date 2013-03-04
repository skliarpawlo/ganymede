$(function() {
    // git stuff
    $("#refresh-repo-btn").click(function() {
        var that = $(this);
        that.prop("disabled","disabled");
        gany.git.reset();
        gany.git.fetch($("#repo-val").val()).done(function(data) {
            that.prop("disabled",false);
            if (data.status == "ok") {
                gany.modals.info( gettext('Repository synchronized') + ": " + data.content );
            } else {
                gany.modals.error( gettext('Error occured') + ": " + data.content );
            }
        });
    });
    $("#repo-val").typeahead({
        source : ["callisto", "huivsto"]
    });

    $("#branch-val").typeahead({
        source : function (q, process) {
            gany.git.branches($("#repo-val").val()).done(function(data) {
                if ( data.length > 0 ) {
                    process( data );
                } else {
                    process( ['master', 'develop'] );
                }
            });
        }
    });

    // tests stuff
    $("#check-all-tests").change( function() {
        if ($(this).is(":checked")) {
            $(this)
                .parents("table")
                .find("tr:visible .test-chk")
                .prop("checked", true);
        } else {
            $(this)
                .parents("table")
                .find("tr:visible .test-chk,tr:visible .subtest-chk,#check-all-subtests")
                .prop("checked", false);
        }
    });

    $("#check-all-subtests").change( function() {
        if ($(this).is(":checked")) {
            $(this)
                .parents("table")
                .find("tr:visible .subtest-chk")
                .prop("checked", true)
                .trigger("change");
        } else {
            $(this)
                .parents("table")
                .find("tr:visible .subtest-chk")
                .prop("checked", false);
        }
    });

    $(".subtest-chk").change( function() {
        var count = $(this).parents("td").find(".subtest-chk:checked").size();
        if (count > 0) {
            $(this).parents("tr").find(".test-chk").prop("checked", true);
        }
    });

    $(".test-chk").change( function() {
        $(this).parents("tr").find(".subtest-chk").prop("checked", false);
    });

    var filter_func = function() {
        var url_filter = $("#filter-pagetest-url").val().toLowerCase();
        var id_filter = $("#filter-pagetest-id").val().toLowerCase();
        var sub_id_filter = $("#filter-subtest-id").val().toLowerCase();
        $(".filtered-pagetest-row").each( function(ind,el) {
            var url = $(el).find(".filtered-pagetest-url").text().toLowerCase();
            var id = $(el).find(".filtered-pagetest-id").text().toLowerCase();
            var sub_id = $(el).find(".filtered-subtest-id").text().toLowerCase();
            if ((url.search(url_filter) == -1) ||
                (id.search(id_filter) == -1) ||
                (sub_id.search(sub_id_filter) == -1)) {
                $(el).hide();
            } else {
                $(el).show();
            }
        });
    };

    $("#filter-pagetest").keyup(filter_func);
    $("#filter-pagetest-url").keyup(filter_func);
    $("#filter-subtest-id").keyup(filter_func);

    // env
    var editor_env = gany.code.block( "env-script", {
        mode : {
            name : "php"
        },
        lineNumbers : true
    });

    // stupid hack to force redraw
    $(".nav-tabs li").click(function(){
        setTimeout( function() {
            editor_env.refresh();
        }, 500);
    });

});