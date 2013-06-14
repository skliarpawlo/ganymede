$(function() {

    var editor_test = gany.code.block("module-source-code", {
        mode : {
            name : "python",
            version : 2
        },
        lineNumbers : true,
        indentUnit: 4
    });

    editor_test.setSize( "100%", 800 );

});