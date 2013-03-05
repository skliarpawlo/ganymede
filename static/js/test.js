$(function() {

    var editor_test = gany.code.block("test-source-code", {
        mode : {
            name : "python",
            version : 2
        },
        lineNumbers : true,
        indentUnit: 4
    });

    $("#template-selector").change(function() {
        var ind = $(this).find("option").index($(this).find(":selected"));
        editor_test.setValue($("#template-block").find('.template-content').eq(ind).text());
        editor_test.refresh();
    });

});