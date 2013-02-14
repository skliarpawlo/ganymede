$(function() {

    var editor_pagetest = gany.code.block("pagetest-source-code", {
        mode : {
            name : "python",
            version : 2
        },
        lineNumbers : true,
        indentUnit: 4
    });

    var editor_subtest = gany.code.block("subtest-source-code", {
        mode : {
            name : "python",
            version : 2
        },
        lineNumbers : true,
        indentUnit: 4
    });

    $("#open-noob-block").click(function(){
        $("#guru-block").hide();
        $("#test-status-block").hide();
        $("#noob-block").show();
    });
    $("#open-guru-block").click(function(){
        $("#noob-block").hide();
        $("#guru-block").show();
        $("#test-status-block").show();
    });

    $("#open-subtest-block").click(function() {
        $("#pagetest-code-block").hide();
        $("#subtest-code-block").show();
        editor_subtest.refresh();
    });

    $("#open-pagetest-block").click(function() {
        $("#subtest-code-block").hide();
        $("#pagetest-code-block").show();
        editor_pagetest.refresh();
    });

});