$(function(){

    var content_refresh = function() {
        var x = gany.urls.parseHashes();
        if (!x.page) {
            x.page = 1;
            x.pagesize = 10;
            window.location = gany.urls.dumpHashes(x);
        }
        $.get("", {page:x.page, pagesize:x.pagesize}).done(function(data){
            console.log($(data).find("tr").size());
            if ($(data).find("tr").size() - 1 < x.pagesize) {
                $("#pagi-next").parents("li").addClass("disabled");
            } else {
                $("#pagi-next").parents("li").removeClass("disabled");
            }
            $("#state-table").html(data);
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
        content_refresh();
        return false;
    });

    $("#pagi-next").click(function() {
        var x = gany.urls.parseHashes();
        if (!x.page)
            x.page = 1;
        x.page = x.page * 1 + 1;
        if (x.page > 1)
            $("#pagi-prev").parents("li").removeClass("disabled");
        $("#page-no").text(x.page);
        location.hash = gany.urls.dumpHashes(x);
        content_refresh();
        return false;
    });
});