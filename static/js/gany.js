var gany = gany || {};

$.extend( gany, (function() {

    $(function() {
        $(".lang-chooser").click( function() {
            var lang = $(this).attr("lang_id");
            $.post("/i18n/setlang/", {
                next : "",
                language : lang
            }, function(data) {
                document.location.reload();
            } );
        });
        $('[data-toggle="tooltip"]').tooltip();
        $('.datetimepicker').each( function( ind, el ) {
            var type = $(el).attr("picker-type");
            var format = $(el).find("input").attr("data-format");
            o = {};
            if (type.indexOf("date") < 0) {
                o.pickDate = false;
            }
            if (type.indexOf("time") < 0) {
                o.pickTime = false;
            }
            if (type.indexOf("nosec") >= 0) {
                o.pickSeconds = false;
            }
            $(el).datetimepicker(o);
        });

        // tabs stuff
        if ( $(".nav-tabs").size() > 0 ) {
            function tabrefresh() {
                var tab = document.location.hash;
                $('.nav-tabs a[href=' + tab + ']').tab('show');
            }
            $(window).on('hashchange', tabrefresh);
            tabrefresh();
        }

    });

    var urls = {
        parseHashes : function( hashes ) {
            if (!hashes)
                hashes = location.hash;
            var p = hashes.slice(1).split("&");
            var res = {};
            for (x in p) {
                if (p[x].length > 0) {
                    var pp = p[x].split("=");
                    res[pp[0]] = pp[1];
                }
            }
            return res;
        },
        dumpHashes : function( params ) {
            var res = [];
            for (x in params) {
                res.push(x + "=" + params[x]);
            }
            return "#" + res.join("&");
        }
    }

    var call = function(method) {
        var args = Array.prototype.slice.call( arguments );
        return $.get( "/ajax/call", {
            package : args[0],
            method : args[1],
            params : JSON.stringify( args.slice( 2 ) )
        } );
    }

    var modals = {
        info : function( info ) {
            $("#info-message").html(info);
            return $("#info-modal").modal("show");
        },
        error : function( info ) {
            $("#error-message").text(info);
            return $("#error-modal").modal("show");
        },
        rusure : function( question, yes ) {
            $("#rusure-question").text( question );
            if ( yes ) {
                $("#rusure-yes").unbind('click').bind('click', function() {
                    yes.apply($("#rusure-modal"));
                });
            }
            return $("#rusure-modal").modal( 'show' );
        }
    }

    var job = {

        gather_data : function() {
            var name = $("#job-name").val();
            // git
            var repo = $("#repo-val").val();
            var branch = $("#branch-val").val();
            // github
            var github = 'no';
            if ($("#chk-github").is(":checked")) {
                github = 'yes';
            }
            // deploy
            var deploy = null;
            if ($("#deploy-code-chbox").is(":checked")) {
                gany.code.block( "deploy-scipt" ).save();
                deploy = $("#deploy-scipt").val();
            }
            // env
            var envs = [];
            $('[data-key="env"]').each( function( ind, el ) {
                var that = $(el);
                var path = that.find('[data-key="env-path"]').val();
                var lang = that.find('[data-key="env-lang"] :selected').val();
                var code = that.find('[data-key="env-script"]').val();
                envs.push( {
                    "path" : path,
                    "lang" : lang,
                    "code" : code
                } );
            } );
            // tests
            var tests = gany.dataprovider.global( "tests_data_provider").checkedlist.all();

            //notification
            var users = [];
            $("[user_id]:checked").each( function( ind, el ) {
                users.push( $(el).attr("user_id") * 1 );
            });

            var exec_time = $("#exec-time").val();

            return {
                name : name,
                repo : repo,
                branch : branch,
                tests : JSON.stringify(tests),
                users : JSON.stringify(users),
                envs : JSON.stringify(envs),
                github : github,
                exec_time : exec_time,
                deploy : deploy
            };
        }

    }

    var task = {

        log : function( id, len, result_count, cur_log_len ) {
            return call( "core.logger", "ajax_read", id, len, result_count, cur_log_len )
        },

        stop_current_task : function() {
            return call("testing_runtime.tasks", "stop_current_task")
        }

    }

    var boxes = {
        error : function( block ) {
            return {
                show : function (infos) {
                    block.find(".content").text( infos.push ? infos.join(", ") : infos );
                    block.find(".close").unbind().bind( 'click', function () {
                        block.hide();
                    });
                    block.slideDown(500);
                }
            }
        }
    }

    var code_cache = {};
    var code = {
        block : function( id, options ) {
            if (!code_cache[ id ]) {
                code_cache[ id ] = CodeMirror.fromTextArea(document.getElementById(id), options);
            }
            return code_cache[ id ];
        }
    }

    var test = {
        gather_data : function() {
            res = {};

            var block = gany.code.block("test-source-code");
            block.save();
            res["code"] = block.getTextArea().value;

            if ($("#test-status").is(":checked")) {
                res["status"] = "new";
            } else {
                res["status"] = "accepted";
            }

            var tags = $("#test-tag-list").tags().getTags();
            res["tags"] = JSON.stringify( tags );

            return res;
        }
    }

    var git = {
        branch_cache : false,
        reset : function() {
            this.branch_cache = false
        },
        clone : function( repo ) {
            return call("core.git", "clone", repo);
        },
        fetch : function( repo ) {
            return call("core.git", "fetch", repo);
        },
        branches : function( repo ) {
            var that = this;
            var branch_deferred = $.Deferred();

            if (that.branch_cache == false) {
                var deferred = call("core.git", "branches", repo);
                deferred.done(function(data) {
                    if (data.status == "ok") {
                        that.branch_cache = data.content;
                        branch_deferred.resolve( that.branch_cache );
                    } else {
                        branch_deferred.resolve( [] );
                    }
                });
            } else {
                branch_deferred.resolve( that.branch_cache );
            }

            return branch_deferred;
        }
    }

    var modules = {
        gather_data : function() {
            var res = {};
            res['name'] = $( "#module-name").val();
            res['path'] = $( "#module-path").val();

            var block = gany.code.block("module-source-code");
            block.save();
            res["code"] = block.getTextArea().value;

            return res;
        }
    }

    return {
        urls : urls,
        test : test,
        code : code,
        modals : modals,
        job : job,
        task : task,
        git : git,
        boxes : boxes,
        modules : modules
    }
})() );