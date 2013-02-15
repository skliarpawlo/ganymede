$(function(){

    var filter_func = function() {
        var url_filter = $("#filter-pagetest-url").val();
        var id_filter = $("#filter-pagetest-id").val();
        $(".filtered-pagetest-row").each( function(ind,el) {
            var url = $(el).find(".filtered-pagetest-url").text();
            var id = $(el).find(".filtered-pagetest-id").text()
            if ((url.search(url_filter) == -1) || (id.search(id_filter) == -1)) {
                $(el).hide();
            } else {
                $(el).show();
            }
        });
    };
    $("#filter-pagetest-url").keyup(filter_func);
    $("#filter-pagetest-id").keyup(filter_func);
});