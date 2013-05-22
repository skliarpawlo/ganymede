$(function() {
    // git stuff
    $("#refresh-repo-btn").click(function() {
        var that = $(this);
        that.find(".icon-refresh").removeClass("icon-refresh").addClass("icon-time");
        gany.git.reset();
        gany.git.fetch($("#repo-val").val()).done(function(data) {
            that.find(".icon-time").removeClass("icon-time").addClass("icon-refresh");
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
                .find("tr:visible .test-chk").each( function( ind, el ) {
                    $(el).prop("checked", true);
                    provider.check( $(el).attr("test_id") * 1 );
                    if ($(el).attr("main_test")) {
                        provider.check( $(el).attr("main_test") * 1 );
                    }
                } );
        } else {
            $(this)
                .parents("table")
                .find("tr:visible .test-chk").each( function( ind, el ) {
                    $(el).prop("checked", false);
                    provider.uncheck( $(el).attr("test_id") * 1 );
                } );
        }
    });

    $("#tests-list").delegate( ".subtest-chk", "change", function() {
        if ($(this).is(":checked")) {
            provider.check( $(this).attr("test_id") * 1 );
            provider.check( $(this).attr("main_test") * 1 );
        } else {
            provider.uncheck( $(this).attr("test_id") * 1 );
        }
        var count = $(this).parents("table").find(".subtest-chk:checked").size();
        if (count > 0) {
            var par = $(this).parents("table").find(".maintest-chk[test_id='" + $(this).attr("main_test") + "']");
            par.prop("checked", true);
        }
    } );

    $("#tests-list").delegate( ".maintest-chk", 'change', function() {
        if ($(this).is(":checked")) {
            provider.check( $(this).attr("test_id") * 1 );
        } else {
            provider.uncheck( $(this).attr("test_id") * 1 );
        }
        var subtests = $(this).parents("table").find(".subtest-chk[main_test='" + $(this).attr("test_id") + "']");
        subtests.prop( "checked", false );
        subtests.each( function( ind, el ) {
            provider.uncheck( $(el).attr( "test_id" ) * 1 );
        } );
    } );

    var test_layout =
        '{{if type=="main"}}' +
            '<tr class="filtered-test-row" test_id="${id}">' +
                '<td>' +
                    '<input type="checkbox" ' +
                           'test_id="${id}" ' +
                           '{{if checked}} checked {{/if}} ' +
                           'class="test-chk maintest-chk"/>' +
                '</td>' +
                '<td>' +
                    '<a class="filtered-test-id" href="${update}">${doc} (#${id})</a>' +
                    '{{if status == "new"}} ' +
                        '<small class="muted">[' + gettext('in development') + ']</small>' +
                    '{{/if}}' +
                '</td>' +
                '<td>' +
                    '<a class="filtered-test-url" href="${url}">${url}</a>' +
                '</td>' +
                '<td>' +
                    '&nbsp' +
                '</td>' +
                '<td>' +
                    '${whose}' +
                '</td>' +
            '</tr>' +
        '{{else}}' +
            '<tr class="filtered-test-row">' +
                '<td>' +
                    '<input main_test="${parent_id}" class="test-chk subtest-chk" ' +
                           'type="checkbox" ' +
                           '{{if checked}} checked {{/if}} ' +
                           'test_id="${id}">' +
                '</td>' +
                '<td>' +
                    '↳ <a class="filtered-test-id" href="${update}">${doc} (#${id})</a> ' +
                    '{{if status == "new"}}<small class="muted">[' + gettext('in development') + ']</small>{{/if}}' +
                '</td>' +
                '<td>&nbsp</td>' +
                '<td>' +
                    '${parent}' +
                '</td>' +
                '<td>' +
                    '${whose}' +
                '</td>' +
            '</tr>' +
        '{{/if}}';

    $.template( "test_layout", test_layout );

    var provider = new gany.dataprovider.DataProvider( tests_data );
    var table = new gany.dataprovider.Table( $( "#tests-list" ), provider );
    $(provider).trigger( "data-changed" );
    gany.dataprovider.global( "tests_data_provider", provider );

    var filter_func = function() {
        provider.pagination.page = 1;
        var filters = [];
        $(".like-filter").each( function( ind, el ) {
            filters.push( new gany.dataprovider.LikeFilter( $(el).attr("data-key"), $(el).val() ) );
        } );
        $(".parent-filter").each( function( ind, el ) {
            filters.push( new gany.dataprovider.ParentFilter( $(el).attr("data-key"), $(el).val() ) );
        } );
        provider.filters = filters;
        $(provider).trigger( "data-changed" );
    };

    $(".like-filter").change( filter_func );
    $(".parent-filter").change( filter_func );

    var pagination_ui = gany.dataprovider.Pagination( $("#pagi-prev"), $("#pagi-next"), $("#page-no"), provider );

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