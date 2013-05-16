$(function(){

    var content_refresh = function() {
        var x = gany.urls.parseHashes();
        if (!x.page) {
            x.page = 1;
            x.pagesize = 25;
            window.location = gany.urls.dumpHashes(x);
        }
        return $.get("", {page:x.page, pagesize:x.pagesize}).done(function(data){
            if ($($.trim(data)).find("tr").size() - 1 < x.pagesize) {
                $("#pagi-next").parents("li").addClass("disabled");
            } else {
                $("#pagi-next").parents("li").removeClass("disabled");
            }
            $("#state-table").html(data);
            $("#loading-block").fadeOut(200);
        });
    }

    setInterval( content_refresh, 2000 );

    $("#pagi-prev").click(function() {
        var x = gany.urls.parseHashes();
        if (x.page > 1)
            x.page = x.page * 1 - 1;
        if (x.page == 1)
            $("#pagi-prev").parents("li").addClass("disabled");
        $("#page-no").text(x.page);
        location.hash = gany.urls.dumpHashes(x);
        $("#loading-block").fadeIn(300);
        content_refresh();
        return false;
    });

    $("#pagi-next").click(function() {
        if ($("#pagi-next").parents("li").hasClass('disabled'))
            return false;
        var x = gany.urls.parseHashes();
        if (!x.page)
            x.page = 1;
        x.page = x.page * 1 + 1;
        if (x.page > 1)
            $("#pagi-prev").parents("li").removeClass("disabled");
        $("#page-no").text(x.page);
        location.hash = gany.urls.dumpHashes(x);
        $("#loading-block").fadeIn(200);
        content_refresh();
        return false;
    });

    // initial page
    var x = gany.urls.parseHashes();
    if (!x.page)
        x.page = 1;
    if (x.page > 1) {
        $("#pagi-prev").parents("li").removeClass("disabled");
        $("#loading-block").fadeIn(200);
        content_refresh();
    }
    $("#page-no").text(x.page);

});