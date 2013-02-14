var gany = (function() {
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
            $("#info-message").text(info);
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
            // env
            gany.code.block("env-script").save();
            var env = $("#env-script").val();
            // tests
            var tests = [];
            $("[test_id]:checked").each( function( ind, el ) {
                tests.push( $(el).attr("test_id") );
            } );

            return {
                name : name,
                repo : repo,
                branch : branch,
                tests : JSON.stringify(tests),
                env : env
            };
        }

    }

    var task = {

        log : function( id, len ) {
            return call("core.logger", "ajax_read", id, len)
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
            if ($("#open-pagetest-block").hasClass("active")) {
                var block = gany.code.block("pagetest-source-code");
                block.save();
                res["code"] = block.getTextArea().value;
            }
            if ($("#open-subtest-block").hasClass("active")) {
                var block = gany.code.block("subtest-source-code");
                block.save();
                res["code"] = block.getTextArea().value;
            }
            if ($("#test-status-new").hasClass("active")) {
                res["status"] = "NEW";
            }
            if ($("#test-status-accepted").hasClass("active")) {
                res["status"] = "ACCEPTED";
            }
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

    return {
        test : test,
        code : code,
        modals : modals,
        job : job,
        task : task,
        git : git,
        boxes : boxes
    }
})();