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

    // deploy stuff

    var code_b = gany.code.block( "deploy-scipt", {
        mode : {
            name : "shell"
        },
        lineNumbers : true
    } );
    // stupid hack to force redraw
    $(".nav-tabs li").click(function(){
        setTimeout( function() {
            code_b.refresh();
        }, 500);
    });

    $("#deploy-code-chbox").change( function() {
        if ($("#deploy-code-chbox").is(":checked")) {
            $("#deploy-code-part").show();
            code_b.refresh();
        } else {
            $("#deploy-code-part").hide();
        }
    } );


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
                .find("tr:visible .test-chk")
                .prop("checked", false);
        }
    });

    $(".subtest-chk").change( function() {
        var count = $(this).parents("table").find(".subtest-chk:checked").size();
        if (count > 0) {
            $(this).parents("table").find(".maintest-chk[test_id='" + $(this).attr("main_test") + "']").prop("checked", true);
        }
    });

    $(".maintest-chk").change( function() {
        $(this).parents("table").find(".subtest-chk[main_test='" + $(this).attr("test_id") + "']").prop("checked", false);
    });

    var filter_func = function() {
        var url_filter = $("#filter-test-url").val().toLowerCase();
        var id_filter = $("#filter-test-id").val().toLowerCase();
        var parent_filter = $("#filter-test-parent").val() * 1;
        $(".filtered-test-row").each( function(ind,el) {
            var url = $(el).find(".filtered-test-url").text().toLowerCase();
            var id = $(el).find(".filtered-test-id").text().toLowerCase();
            var parent = $(el).find(".filtered-test-parent").text() * 1;
            if ((url.search(url_filter) == -1) ||
                (id.search(id_filter) == -1) ||
                (parent_filter != 0 && parent != parent_filter) ) {
                $(el).hide();
            } else {
                $(el).show();
            }

            if ((url.search(url_filter) != -1) &&
                (id.search(id_filter) != -1) &&
                ($(el).attr("test_id") * 1 == parent_filter)) {
                $(el).show()
            }
        });
    };

    $("#filter-test-id").keyup(filter_func);
    $("#filter-test-url").keyup(filter_func);
    $("#filter-test-parent").change(filter_func);

    // env
    var bind_env_events = function( env_el ) {
        var that = env_el;
        var lang = that.find('[data-key="env-lang"] :selected').val();
        var code = that.find('[data-key="env-script"]').get(0);
        var code_ui = CodeMirror.fromTextArea(code, {
            mode : {
                name : lang
            },
            lineNumbers : true
        });

        code_ui.on( "change", function( that ) {
            that.save();
        } );

        that.find('[data-key="env-delete"]').click( function() {
            that.remove();
        });

        // stupid hack to force redraw
        $(".nav-tabs li").click(function(){
            setTimeout( function() {
                code_ui.refresh();
            }, 500);
        });
    }

    $('[data-key="env"]').each( function( ind, el ) {
        bind_env_events( $( el ) );
    } );

    $("#add-env").click( function() {
        var new_el = $(
            "<tr data-key='env'>" +
                $('[data-key="sample"]').html() +
            "</tr>"
        );
        $("#envs-table").append( new_el );
        bind_env_events( new_el );
    } );

});