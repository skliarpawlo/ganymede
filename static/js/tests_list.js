$(function(){

    var filter_func = function() {
        var url_filter = $("#filter-test-url").val().toLowerCase();
        var id_filter = $("#filter-test-id").val().toLowerCase();
        var sub_id_filter = $("#filter-test-id").val().toLowerCase();
        $(".filtered-test-row").each( function(ind,el) {
            var url = $(el).find(".filtered-test-url").text().toLowerCase();
            var id = $(el).find(".filtered-test-id").text().toLowerCase();
            if ((url.search(url_filter) == -1) ||
                (id.search(id_filter) == -1)) {
                $(el).hide();
            } else {
                $(el).show();
            }
        });
    };
    $("#filter-test-url").keyup(filter_func);
    $("#filter-test-id").keyup(filter_func);

    $(".remove-test").click( function() {
        var that = $(this);
        var test_id = $(this).parents("tr,li").attr("test_id");
        gany.modals.rusure( gettext('Are you sure want to delete test') + " " + test_id + " ?", function() {
            this.modal('hide');
            $.post("/test/remove", { test_id : test_id }, function(data) {
                if (data.status == "ok") {
                    that.parents("tr,li").first().remove();
                } else {
                    gany.modals.error(gettext('Error occured') + ": " + data.content);
                }
            });
        });
    });
});