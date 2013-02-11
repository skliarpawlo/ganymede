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
        rusure : {
            show : function( question, yes ) {
                $("#rusure-question").text( question );
                $("#rusure-modal").modal( 'show' );
                if ( yes ) {
                    $("#rusure-yes").unbind('click').bind('click', yes);
                }
            }
        }
    }

    var job = {

        gather_data : function() {
            var name = $("#job-name").val();
            // git
            var repo = $("#repo-val").val();
            var branch = $("#branch-val").val();
            // env
            var env = $("#env-script").val();
            // tests
            var tests = {};
            $("[test_id]").each( function( ind, el ) {
                var subdata = [];
                var test_el = $( el );
                $("[subtest_id]:checked", test_el).each( function( ind, subel ) {
                    subdata.push( $(subel).attr( "subtest_id" ) );
                } );
                tests[ $( el ).attr( "test_id" ) ] = subdata;
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

    var git = {
        clone : function( repo ) {
            return call("core.git", "clone", repo);
        },
        branches : function( repo ) {
            return call("core.git", "branches", repo);
        }
    }

    return {
        modals : modals,
        job : job,
        git : git
    }
})();