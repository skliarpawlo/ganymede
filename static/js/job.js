$(function() {
    // git stuff
    $("#repo-val").typeahead({
        source : ["callisto", "huivsto"]
    });
    $("#branch-val").typeahead({
        source : function (q, process) {
            gany.git.branches($("#repo-val").val()).done(function(data) {
                var ans = $.parseJSON(data);
                if (ans.status == "ok") {
                    process( ans.content );
                } else {
                    process( ['master', 'develop'] );
                }
            });
        }
    });

    // tests stuff
    $("#check-all-tests").change( function() {
        if ($(this).attr("checked")) {
            $(this).parents("table").find(".test-chk").attr("checked", "checked");
        } else {
            $(this).parents("table").find(".test-chk,.subtest-chk,#check-all-subtests").removeAttr("checked");
        }
    });

    $("#check-all-subtests").change( function() {
        if ($(this).attr("checked")) {
            $(this).parents("table").find(".subtest-chk").attr("checked", "checked").trigger("change");
        } else {
            $(this).parents("table").find(".subtest-chk").removeAttr("checked");
        }
    });

    $(".subtest-chk").change( function() {
        var count = $(this).parents("td").find(".subtest-chk:checked").size();
        if (count > 0) {
            $(this).parents("tr").find(".test-chk").attr("checked", "checked");
        }
    });
});