$(function() {
    // git stuff
    $("#refresh-repo-btn").click(function() {
        var that = $(this);
        that.prop("disabled","disabled");
        gany.git.reset();
        gany.git.fetch($("#repo-val").val()).done(function(data) {
            that.prop("disabled",false);
            if (data.status == "ok") {
                gany.modals.info( "Репозиторий обновлен : " + data.content );
            } else {
                gany.modals.error( "Возникла ошибка:" + data.content );
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

    $("#filter-pagetest").keyup(function(){
        var filter = $("#filter-pagetest").val();
        $(".filtered-pagetest").each( function(ind,el) {
            if ($(el).text().search(filter) == -1) {
                $(el).parents(".filtered-pagetest-row").hide();
            } else {
                $(el).parents(".filtered-pagetest-row").show();
            }
        });
    });

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