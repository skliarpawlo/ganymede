$(function() {

    var editor_test = gany.code.block("test-source-code", {
        mode : {
            name : "python",
            version : 2
        },
        lineNumbers : true,
        indentUnit: 4
    });

    $("#template-selector button").click(function() {
        editor_test.setValue($(this).next().text());
        editor_test.refresh();
    });

});