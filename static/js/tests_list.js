$(function(){

    var filter_func = function() {
        var url_filter = $("#filter-pagetest-url").val().toLowerCase();
        var id_filter = $("#filter-pagetest-id").val().toLowerCase();
        $(".filtered-pagetest-row").each( function(ind,el) {
            var url = $(el).find(".filtered-pagetest-url").text().toLowerCase();
            var id = $(el).find(".filtered-pagetest-id").text().toLowerCase();
            if ((url.search(url_filter) == -1) || (id.search(id_filter) == -1)) {
                $(el).hide();
            } else {
                $(el).show();
            }
        });
    };
    $("#filter-pagetest-url").keyup(filter_func);
    $("#filter-pagetest-id").keyup(filter_func);

    $(".remove-test").click( function() {
        var that = $(this);
        var test_id = $(this).parents("tr").attr("test_id");
        gany.modals.rusure( "Уверенны что хотите удалить тест " + test_id + " (вместе с подтестами)?", function() {
            this.modal('hide');
            $.post("/test/remove", { test_id : test_id }, function(data) {
                if (data.status == "ok") {
                    that.parents("tr").remove();
                } else {
                    gany.modals.error("Возникла ошибка: " + data.content);
                }
            });
        });
    });
});