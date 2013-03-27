$(function(){

    var filter_func = function() {
        var url_filter = $("#filter-test-url").val().toLowerCase();
        var id_filter = $("#filter-test-id").val().toLowerCase();
        var parent_filter = $("#filter-test-parent").val() * 1;
        $(".filtered-test-row").each( function(ind,el) {
            var url = $(el).find(".filtered-test-url").text().toLowerCase();
            var id = $(el).find(".filtered-test-id").text().toLowerCase();
            var parent = $(el).find(".filtered-test-parent").text() * 1;
            if ((url.search(url_filter) == -1) ||
                (id.search(id_filter) == -1) ||
                (parent_filter != 0 && parent != parent_filter) ) {
                $(el).hide();
            } else {
                $(el).show();
            }

            if ((url.search(url_filter) != -1) &&
                (id.search(id_filter) != -1) &&
                ($(el).attr("test_id") * 1 == parent_filter)) {
                $(el).show()
            }
        });
    };
    $("#filter-test-url").keyup(filter_func);
    $("#filter-test-id").keyup(filter_func);
    $("#filter-test-parent").change(filter_func);

    $(".remove-test").click( function() {
        var that = $(this);
        var test_id = $(this).parents("tr,li").attr("test_id");
        gany.modals.rusure( gettext('Are you sure want to remove test') + " " + test_id + " ?", function() {
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